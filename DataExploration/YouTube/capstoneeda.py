# -*- coding: utf-8 -*-
"""CapstoneEDA.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1YgFmB9Dd9juPvp4dYviYfdoRmVS1V5mL
"""

# upload LanguageIdentifiedComments.csv
from google.colab import files
uploaded = files.upload()

import io
import pandas as pd
data = pd.read_csv(io.BytesIO(uploaded['LanguageIdentifiedComments.csv']))

data.describe()

data.head()

# Add column names to the DataFrame
column_names = ['Comment', 'IndicLID Code', 'Score','Model']

# Set the column names of the DataFrame
# Parameters:
#   column_names (list of str): List containing the names of the columns.
# Returns:
#   None
# Note:
#   This function assigns the specified column names to the DataFrame.
data.columns = column_names

# Display the first 15 rows of the DataFrame
data.head(15)

# Calculate the number of null values for each column in the DataFrame.
# Returns:
#   pandas.Series: A Series containing the count of null values for each column.
null_counts = data.isnull().sum()
print(null_counts)

# Removes rows with null values in the specified columns.

# Parameters:
#   data (pd.DataFrame): The DataFrame containing the data.
#   column_names (list of str): A list of column names to check for null values.
# Returns:
#   A DataFrame with rows containing null values in the specified columns removed.

column_names= ['Comment', 'IndicLID Code']
data = data.dropna(subset=column_names, how='any')

# There are no null values left in the dataframe
null_counts = data.isnull().sum()
print(null_counts)

# Retrieves the counts of unique values in the 'IndicLID Code' column of the DataFrame
data['IndicLID Code'].value_counts()

import pandas as pd

# Count the occurrences of each language
language_counts = data['IndicLID Code'].value_counts()

# Convert to DataFrame
language_counts_df = pd.DataFrame(language_counts.reset_index())
language_counts_df.columns = ['Language', 'Count']

# Save DataFrame to CSV file
language_counts_df.to_csv('language_counts.csv', index=False)

"""Bar plot of Language Distribution"""

import matplotlib.pyplot as plt

# Count the occurrences of each language
language_counts = data['IndicLID Code'].value_counts()

# Plotting the language distribution
plt.figure(figsize=(15, 5))
language_counts.plot(kind='bar', color='skyblue')
plt.title('Language Distribution')
plt.xlabel('Language')
plt.ylabel('Count')

# Saving the plot as an image file
plt.savefig('YoutubeCommentsLanguageDistribution.png')

# Displaying the plot
plt.show()

import matplotlib.pyplot as plt

# Get the top 5 language counts
top_language_counts = data['IndicLID Code'].value_counts().head(5)


# Plotting the language distribution
plt.figure(figsize=(10, 5))
top_language_counts.plot(kind='bar', color='skyblue')
plt.title('Top 5 Language Distribution')
plt.xlabel('Language')
plt.ylabel('Count')

# Add count labels on top of each bar
for i, count in enumerate(top_language_counts):
    plt.text(i, count + 0.1, str(count), ha='center', va='bottom')

plt.savefig('Top5_YoutubeCommentsLanguageDistribution.png')
plt.show()

comments = pd.DataFrame(data['Comment'])

comments.describe()

# preprocessing the comments
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import re

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

def preprocess_text(text):
    """
    Preprocesses the input text by converting it to lowercase, removing URLs, tokenizing,
    removing stopwords, lemmatizing, and joining back into a single string.

    Args:
        text (str): The input text to be preprocessed.

    Returns:
        str: The preprocessed text.
    """
    if pd.notna(text):
        text = text.lower()
        text = re.sub(r'https?://\S+', '', text)
        tokens = word_tokenize(text)
        tokens = [word for word in tokens if word.isalnum()]
        stop_words = set(stopwords.words('english'))
        tokens = [word for word in tokens if word not in stop_words]
        lemmatizer = WordNetLemmatizer()
        tokens = [lemmatizer.lemmatize(word) for word in tokens]
        preprocessed_text = ' '.join(tokens)
    else:
        preprocessed_text = ''
    return preprocessed_text

# Create a DataFrame to store the preprocessed comments
preprocessedComments = pd.DataFrame()

# Apply the preprocess_text function to each comment in the 'Comment' column
# and store the result in the 'comments' column of preprocessedComments
preprocessedComments['comments'] = comments['Comment'].apply(preprocess_text)
print(preprocessedComments)

preprocessedComments.head()

"""Word Cloud"""

from wordcloud import WordCloud

# Concatenate all preprocessed comments into a single string
text = " ".join(comment for comment in preprocessedComments['comments'])
# Generate the word cloud object
wordcloud = WordCloud(background_color="white").generate(text)

# Plot and display the word cloud
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis("off")

# Save the word cloud as an image
plt.savefig('YoutubeCommentsWordCloud.png')
plt.show()

# Display the keys of the word cloud dictionary
print(wordcloud.words_.keys())

# bar plot for the top 15 words
from collections import Counter

# Calculate the frequency of each word in the word cloud
frequency = wordcloud.words_

# Sort the word frequencies in descending order
sortedFrequency = dict(sorted(frequency.items(), key=lambda x: x[1], reverse=True))

# Extract the top 15 words and their frequencies
topWords = list(sortedFrequency.keys())[:15]
topFreq = [sortedFrequency[word] for word in topWords]

# Create a bar plot
plt.figure(figsize=(15, 6))
plt.bar(topWords, topFreq, color='skyblue')
plt.xlabel('Words')
plt.ylabel('Frequency')
plt.title('Top 15 Word Frequencies')
plt.xticks(rotation=45)

# Save the plot as an image file
plt.savefig('YoutubeCommentsTop15WordFrequencies.png')

# Display the plot
plt.show()