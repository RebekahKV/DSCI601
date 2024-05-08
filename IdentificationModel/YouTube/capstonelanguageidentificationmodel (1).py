# -*- coding: utf-8 -*-
"""CapstoneLanguageIdentificationModel.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1D7uu7-qOmiVhFhWaSSydAGR08hwm5D7Y

# Using IndicLID for Language Identification

Install and Import IndicLID
"""

!pip3 install fasttext
!pip3 install transformers

!git clone https://github.com/AI4Bharat/IndicLID.git

# Commented out IPython magic to ensure Python compatibility.
# %cd "/content/IndicLID/Inference"

# Commented out IPython magic to ensure Python compatibility.
# %mkdir models
# %cd "/content/IndicLID/Inference/models"

!wget https://github.com/AI4Bharat/IndicLID/releases/download/v1.0/indiclid-bert.zip
!wget https://github.com/AI4Bharat/IndicLID/releases/download/v1.0/indiclid-ftn.zip
!wget https://github.com/AI4Bharat/IndicLID/releases/download/v1.0/indiclid-ftr.zip

!unzip indiclid-bert.zip
!unzip indiclid-ftn.zip
!unzip indiclid-ftr.zip

# Commented out IPython magic to ensure Python compatibility.
# %cd "/content/IndicLID/"
# %cd "/content/IndicLID/Inference"

from ai4bharat.IndicLID import IndicLID
IndicLID_model = IndicLID(input_threshold = 0.5, roman_lid_threshold = 0.6)

"""Upload the Comment File for Language Identification"""

# upload AllComments.csv
from google.colab import files
uploaded = files.upload()

import io
import pandas as pd

# stores comments in a dataframe
df = pd.read_csv(io.BytesIO(uploaded['AllComments.csv']))

# Display the first few rows of the DataFrame.
df.head()

# Retrieves the 'text' column data from the DataFrame and converts it to a list.
# Parameters:
#   df (pandas.DataFrame): The DataFrame containing the 'text' column.
# Returns:
#   list: A list containing the data from the 'text' column.
data = df['text'].tolist()

# Convert each element in the data list to a string
# Parameters:
#   data (list): The list containing elements to be converted to strings.
# Returns:
#   list: A list containing the converted strings.
comments = [str(text) for text in data]

# Remove newline characters from each comment in the list.
# Parameters:
#   comments (list of str): The list of comments.
# Returns:
#   list of str: The list of comments with newline characters removed.
comments = [comment.replace('\n', '') for comment in comments]

# Set the batch size for prediction
batch_size = 1
# Perform batch prediction using the IndicLID_model
# Parameters:
#   commentsNew (list): List of comments to be predicted.
#   batch_size (int): The size of each batch for prediction.
# Returns:
#   outputs comments, language identified, score and model used
outputs = IndicLID_model.batch_predict(commentsNew, batch_size)

allComments = pd.DataFrame(outputs)
allComments.head()

# stores data in a .csv file
allComments.to_csv('LanguageIdentifiedCommentsNew.csv', index=False)