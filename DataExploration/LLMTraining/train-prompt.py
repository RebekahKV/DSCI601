import numpy as np
import pandas as pd
import os
from tqdm import tqdm
import bitsandbytes as bnb
import torch
import torch.nn as nn
import transformers
from datasets import Dataset
from peft import LoraConfig, PeftConfig
from trl import SFTTrainer
from trl import setup_chat_format
from transformers import (AutoModelForCausalLM, 
                          AutoTokenizer, 
                          BitsAndBytesConfig, 
                          TrainingArguments, 
                          pipeline, 
                          logging)
from sklearn.metrics import (accuracy_score, 
                             classification_report, 
                             confusion_matrix)
from datetime import datetime

# from sklearn.model_selection import train_test_split
def generate_prompt(data_point):
    return f"""
  Classify the comment into Negative, Neutral, Positive, and return the answer as the corresponding sentiment label.
  text: {data_point["Comment"]}
  label: {data_point["Sentiment"]}""".strip()

def generate_test_prompt(data_point):
    return f"""
      Classify the comment into Negative, Neutral, Positive, and return the answer as the corresponding sentiment label.
      text: {data_point["Comment"]}
      label: """.strip()
      
train_df = pd.read_csv("/home/sd3528/delhi-pollution/dataset/sentiment_train.csv")
val_df = pd.read_csv("/home/sd3528/delhi-pollution/dataset/sentiment_val.csv")
test_df = pd.read_csv("/home/sd3528/delhi-pollution/dataset/sentiment_test.csv")

train_df.columns = train_df.columns.str.strip()  
val_df.columns = val_df.columns.str.strip()

train_df["Comment"] = train_df["Comment"].fillna("").astype(str)
val_df["Comment"] = val_df["Comment"].fillna("").astype(str)
test_df["Comment"] = test_df["Comment"].fillna("").astype(str)
train_df['Sentiment'] = train_df['Sentiment'].apply(lambda x: x.lower())
val_df['Sentiment'] = val_df['Sentiment'].apply(lambda x: x.lower())
test_df['Sentiment'] = test_df['Sentiment'].apply(lambda x: x.lower())

train_df['prompt'] = train_df.apply(generate_prompt, axis=1)
val_df['prompt'] = val_df.apply(generate_test_prompt, axis=1)
test_df['prompt'] = test_df.apply(generate_test_prompt, axis=1)

bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_use_double_quant=False,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype="float16",
)


RUN_NAME = "llama3-8b-qlora-prompt"
model_name = "meta-llama/Meta-Llama-3-8B"
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    device_map="auto",
    torch_dtype="float16",
    quantization_config=bnb_config, 
)

model.config.use_cache = False
model.config.pretraining_tp = 1

tokenizer = AutoTokenizer.from_pretrained(model_name)

tokenizer.pad_token_id = tokenizer.eos_token_id

def predict(test, model, tokenizer):
    y_pred = []
    categories = ["negative", "neutral", "positive"]
    
    for i in tqdm(range(len(test))):
        prompt = test.iloc[i]["prompt"]
        pipe = pipeline(task="text-generation", 
                        model=model, 
                        tokenizer=tokenizer, 
                        max_new_tokens=2, 
                        temperature=0.1)
        
        result = pipe(prompt)
        answer = result[0]['generated_text'].split("label:")[-1].strip()
        
        # Determine the predicted category
        for category in categories:
            if category.lower() in answer.lower():
                y_pred.append(category)
                break
        else:
            y_pred.append("none")
    
    return y_pred
  
def evaluate(y_true, y_pred):
    labels = ["negative", "neutral", "positive"]
    mapping = {label: idx for idx, label in enumerate(labels)}
    
    def map_func(x):
        return mapping.get(x, -1)  # Map to -1 if not found, but should not occur with correct data
    
    y_true_mapped = np.vectorize(map_func)(y_true)
    y_pred_mapped = np.vectorize(map_func)(y_pred)
    
    # Calculate accuracy
    accuracy = accuracy_score(y_true=y_true_mapped, y_pred=y_pred_mapped)
    print(f'Accuracy: {accuracy:.3f}')
    
    # Generate accuracy report
    unique_labels = set(y_true_mapped)  # Get unique labels
    
    for label in unique_labels:
        label_indices = [i for i in range(len(y_true_mapped)) if y_true_mapped[i] == label]
        label_y_true = [y_true_mapped[i] for i in label_indices]
        label_y_pred = [y_pred_mapped[i] for i in label_indices]
        label_accuracy = accuracy_score(label_y_true, label_y_pred)
        print(f'Accuracy for label {labels[label]}: {label_accuracy:.3f}')
        
    # Generate classification report
    class_report = classification_report(y_true=y_true_mapped, y_pred=y_pred_mapped, target_names=labels, labels=list(range(len(labels))))
    print('\nClassification Report:')
    print(class_report)
    
    # Generate confusion matrix
    conf_matrix = confusion_matrix(y_true=y_true_mapped, y_pred=y_pred_mapped, labels=list(range(len(labels))))
    print('\nConfusion Matrix:')
    print(conf_matrix)


## Zero-shot classification

  # y_pred = predict(test_df[:50], model, tokenizer)
  # y_true = test_df["Sentiment"].values

  # evaluate(y_true[:50], y_pred)
###

def find_all_linear_names(model):
    cls = bnb.nn.Linear4bit
    lora_module_names = set()
    for name, module in model.named_modules():
        if isinstance(module, cls):
            names = name.split('.')
            lora_module_names.add(names[0] if len(names) == 1 else names[-1])
    if 'lm_head' in lora_module_names:  # needed for 16 bit
        lora_module_names.remove('lm_head')
    return list(lora_module_names)
  
modules = find_all_linear_names(model)
output_dir="/home/sd3528/delhi-pollution/sentiment/"+ RUN_NAME 

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

peft_config = LoraConfig(
    lora_alpha=16,
    lora_dropout=0,
    r=64,
    bias="none",
    task_type="CAUSAL_LM",
    target_modules=modules,
)

training_arguments = TrainingArguments(
    output_dir=output_dir,                    # directory to save and repository id
    num_train_epochs=1,                       # number of training epochs
    per_device_train_batch_size=1,            # batch size per device during training
    gradient_accumulation_steps=8,            # number of steps before performing a backward/update pass
    gradient_checkpointing=True,              # use gradient checkpointing to save memory
    optim="paged_adamw_32bit",
    logging_steps=1,                         
    learning_rate=2e-4,                       # learning rate, based on QLoRA paper
    weight_decay=0.001,
    fp16=True,
    bf16=False,
    max_grad_norm=0.3,                        # max gradient norm based on QLoRA paper
    max_steps=-1,
    warmup_ratio=0.03,                        # warmup ratio based on QLoRA paper
    group_by_length=False,
    lr_scheduler_type="cosine",               # use cosine learning rate scheduler
    report_to="wandb",                  # report metrics to w&b
    eval_strategy="steps",              # save checkpoint every epoch
    eval_steps = 0.2,
    run_name=RUN_NAME+str(datetime.now().strftime("%Y-%m-%d_%H-%M-%S")),
)

train_data = Dataset.from_pandas(train_df[['prompt']])
eval_data = Dataset.from_pandas(val_df[['prompt']])

trainer = SFTTrainer(
    model=model,
    args=training_arguments,
    train_dataset=train_data,
    eval_dataset=eval_data,
    peft_config=peft_config,
    dataset_text_field="prompt",
    tokenizer=tokenizer,
    max_seq_length=512,
    packing=False,
    dataset_kwargs={
    "add_special_tokens": False,
    "append_concat_token": False,
    },
)

trainer.train()

trainer.save_model(output_dir)
tokenizer.save_pretrained(output_dir)


"""
Model trained by Soumyajit Datta
"""

