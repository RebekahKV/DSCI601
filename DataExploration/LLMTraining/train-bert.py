import torch
from transformers import BertTokenizer, BertForSequenceClassification
from torch.utils.data import Dataset, DataLoader
from sklearn.model_selection import train_test_split
import torch.nn.functional as F
from torch.optim import AdamW
import pandas as pd

train_df = pd.read_csv("/home/sd3528/delhi-pollution/dataset/sentiment_train.csv")
test_df = pd.read_csv("/home/sd3528/delhi-pollution/dataset/sentiment_val.csv")

train_df.columns = train_df.columns.str.strip()  
test_df.columns = test_df.columns.str.strip()

train_df["Comment"] = train_df["Comment"].fillna("").astype(str)
test_df["Comment"] = test_df["Comment"].fillna("").astype(str)

train_df = train_df.dropna(subset=["Sentiment"])
test_df = test_df.dropna(subset=["Sentiment"])

label_map = {"Negative": 0, "Neutral": 1, "Positive": 2, "negative": 0, "neutral": 1, "positive": 2}
train_df["Sentiment"] = train_df["Sentiment"].map(label_map).astype(int)
test_df["Sentiment"] = test_df["Sentiment"].map(label_map).astype(int)

train_texts = train_df["Comment"].tolist()
train_labels = train_df["Sentiment"].tolist()
val_texts = test_df["Comment"].tolist()
val_labels = test_df["Sentiment"].tolist()

# 2. Tokenize the data using BERT tokenizer
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')

# Tokenize and encode texts
train_encodings = tokenizer(train_texts, truncation=True, padding=True, max_length=128)
val_encodings = tokenizer(val_texts, truncation=True, padding=True, max_length=128)

# 3. Create a custom Dataset class
class TextDataset(Dataset):
    def __init__(self, encodings, labels):
        self.encodings = encodings
        self.labels = labels

    def __getitem__(self, idx):
        item = {key: torch.tensor(val[idx]) for key, val in self.encodings.items()}
        item['labels'] = torch.tensor(self.labels[idx])
        return item

    def __len__(self):
        return len(self.labels)

# Create PyTorch Datasets
train_dataset = TextDataset(train_encodings, train_labels)
val_dataset = TextDataset(val_encodings, val_labels)

# 4. Load BERT model for sequence classification
model = BertForSequenceClassification.from_pretrained('bert-base-uncased', num_labels=3)

# Move model to GPU if available
device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
model.to(device)

# 5. Set up the DataLoader, Optimizer, and Loss function
train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)
val_loader = DataLoader(val_dataset, batch_size=32, shuffle=False)

optimizer = AdamW(model.parameters(), lr=5e-5)  # Learning rate

# 6. Train the BERT model
def train_model(model, train_loader, val_loader, epochs=10):
    model.train()
    for epoch in range(epochs):
        total_train_loss = 0
        correct = 0
        total = 0
        for batch in train_loader:
            # Move batch to the device
            input_ids = batch['input_ids'].to(device)
            attention_mask = batch['attention_mask'].to(device)
            labels = batch['labels'].to(device)

            # Clear previous gradients
            optimizer.zero_grad()

            # Forward pass
            outputs = model(input_ids, attention_mask=attention_mask, labels=labels)
            loss = outputs.loss
            logits = outputs.logits

            # Backpropagation
            loss.backward()
            optimizer.step()

            total_train_loss += loss.item()
            preds = torch.argmax(logits, dim=1)
            correct += (preds == labels).sum().item()
            total += labels.size(0)

        avg_train_loss = total_train_loss / len(train_loader)
        train_accuracy = correct / total

        print(f"Epoch {epoch + 1}/{epochs} | Train Loss: {avg_train_loss:.4f} | Train Accuracy: {train_accuracy:.4f}")

        # Validate the model
        validate_model(model, val_loader)

def validate_model(model, val_loader):
    model.eval()
    correct = 0
    total = 0
    total_val_loss = 0
    with torch.no_grad():
        for batch in val_loader:
            input_ids = batch['input_ids'].to(device)
            attention_mask = batch['attention_mask'].to(device)
            labels = batch['labels'].to(device)

            outputs = model(input_ids, attention_mask=attention_mask, labels=labels)
            loss = outputs.loss
            logits = outputs.logits

            total_val_loss += loss.item()
            preds = torch.argmax(logits, dim=1)
            correct += (preds == labels).sum().item()
            total += labels.size(0)

    avg_val_loss = total_val_loss / len(val_loader)
    val_accuracy = correct / total
    print(f"Validation Loss: {avg_val_loss:.4f} | Validation Accuracy: {val_accuracy:.4f}")

# Train the model
train_model(model, train_loader, val_loader, epochs=10)

# 7. Save the trained model
model.save_pretrained('bert_classifier_model')
tokenizer.save_pretrained('bert_classifier_model')



"""
Model trained by Soumyajit Datta
"""

