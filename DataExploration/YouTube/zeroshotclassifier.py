# -*- coding: utf-8 -*-
"""ZeroShotClassifier.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1gvr5qCC3RiWyBGWVCbsVJgqZkaiRQsfn
"""

import pandas as pd
import numpy as np

comments = pd.read_csv('/content/Comments5000.csv')
comments.head()

import pandas as pd
from transformers import pipeline
import torch

# Check if GPU is available
device = 0 if torch.cuda.is_available() else -1
print("Using", "GPU" if device == 0 else "CPU")

# Load the data
data = pd.read_csv('Comments5000.csv')

# Define the zero-shot classification model and sentiment analysis model
classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli", device=device)
sentiment_analyzer = pipeline("sentiment-analysis", device=device)

sentiment_analyzer = pipeline("sentiment-analysis", model="cardiffnlp/twitter-roberta-base-sentiment-latest", device=device)


# Define factors for classification
factors = [
    "Government", "Atmospheric conditions", "None", "Firecrackers", "Population",
    "Industrial Emission", "Stubble burning", "Farming practices", "Air purifier",
    "Vehicle Emission", "Waste disposal", "Construction", "Smoking",
    "Chemicals", "Festival celebration", "Dust", "Fire",
    "Deforestation", "Burning fossil fuel"]

# Factors for classification
data['Factor'] = data['Comment'].apply(lambda x: classifier(x, candidate_labels=factors)['labels'][0])

data['Sentiment'] = data['Comment'].apply(lambda x: sentiment_analyzer(x)[0]['label'])

data.to_csv('delhi_air_pollution_sentiment_ZS.csv', index=False)
print(data.head())