# DSCI601
## Data Collection
## Reddit data:
Reddit Data Retrieval

### Overview
This project utilizes the Python Reddit API Wrapper (PRAW) to scrape Reddit posts and comments based on specific keywords within certain subreddits. The data is then saved in JSON format. This script is designed to to gather discussions from various dates and subreddits.

### Prerequisites
- Python 3.6 or later
- pip (Python package installer)

### Installation Instructions
Set up a developer account on Reddit to get the API token herw:  [https://www.reddit.com/prefs/apps](url)

Follow the below steps or go here: [https://www.educative.io/courses/reddit-api-python/get-started-with-the-reddit-api](url)
1) Click on the "are you a developer? create an app..." button.
 In the fields, add the following information.
 Add the name of your application.
 Select the option of choice.
 Add the "description" (optional).
2) Skip the "about url".
3) Add the URL in the widget below in the "redirect uri" field.
```
{{EDUCATIVE_LIVE_VM_URL}}
```
4) URL for the redirect URI
 Click on the "create app" button.
 Once the application has been created, copy the "secret" and the "personal use script" token in the widget below,. These will be called CLIENT_SECRET and CLIENT_ID    respectively throughout the course.

### Clone the Repository
To get started, clone this repository to your local system:

#### Install Required Packages:
Install the necessary Python packages using pip:
```
!pip install praw --quiet
```

#### Configuration

You must configure the script with your Reddit API credentials. Create a file named secrets.py in the root directory and add the following:
```
# secrets.py
CLIENT_ID = 'your_client_id'
CLIENT_SECRET = 'your_client_secret'
REDDIT_USERNAME = 'your_reddit_username'
REDDIT_PASSWORD = 'your_reddit_password'
USER_AGENT = 'platform:app_id:version (by /u/yourusername)'
```
Important: Ensure secrets.py is listed in your .gitignore to prevent sharing your credentials publicly.

#### Usage

To run the script, navigate to the directory containing your script and execute:
```
python DataCollection/Reddit/Reddit_Data_Retrieval_Date_and_Keywords_2.ipynb 
```
### Interface
<!-- colab integratation on running the model on custom input python script -->
Inference Notebook --> [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1uoHGHnASpKln1X7t_RJJgNchRsylurNI?usp=sharing)

#### Modifying Search Criteria
Edit the subreddit_names and keywords in the script to tailor the search to your interests. These lists determine which subreddits are searched and what keywords are looked for.

#### Data Output

The script saves the scraped data in JSON format in the project directory. Each file is named after the subreddit it contains data from.

## YouTube data:
You first need to create a YouTube API key. 
You can find step-by-step instructions here: [https://www.youtube.com/watch?v=jykW3AX8pEE](url)
Or follow the steps below:
1) Go to [https://console.cloud.google.com/projectselector2/apis/dashboard?supportedpurview=project](url)
2) Click "Select a project"
3) Click "New Project" -> Add project name: example "DSCI601" ->  Organization: "g.rit.edu" -> Click "Create"
4) Next go to Library (located on the left under "APIs & Services")
5) Search "youtube data api v3" then click on it
6) Click "Enable"
7) Click "Credentials" (located on the left under "APIs & Services YouTube Data API v3")
8) Click "Create Credentials" ->  "API Key" 
9) Copy the API key and save it in a text file Key.txt

### Prerequisites
- Python 3.6 or later
- pip (Python package installer)
- Google Chrome: [https://www.google.com/chrome/](url)

### In Terminal:
Create a new directory: mkdir dsci601project
Download all the files in this directory and save Key.txt here.

Install selenium using pip: 
```
pip install selenium
```
Download Chromedriver and store it in the directory created for this project "dsci601project":
1) [https://chromedriver.chromium.org/downloads](url)
2) Check Google Chrome Version by clicking the 3 dots in the right hand corner then go to  Help -> About Google Chrome
3) Look for the Chrome Driver which is compatible with the Google Chrome installed.

### Extracting Comments:

Using DownloadVideoURLsFromSearchQuery.py, you can download video urls for a given YouTube search query. 
First Search Query: "Delhi air pollution news" save to csv "AirPollutionNews.csv"
Second Search Query: "Delhi air pollution" save to csv "AirPollutionVideos.csv"

In order to use a new search query, change line 68. 
In order to save the CSV to a new location, change line 56. 

To Extract video IDs only, use CapstonExtractVideoIds.py to generate "VideoIDs.txt" and "VideoIDs1.txt"

To obtain the video metadata, first create two folders in the same directory with name example: AirPollutionVideoMetadata and AirPollutionNewsMetadata
The python command to download video metadata will be:
```
python DownloadVideoMetadata.py c VideoIDs.txt AirPollutionVideoMetadata Key.txt
```
```
python DownloadVideoMetadata.py c VideoIDs1.txt AirPollutionNewsMetadata Key.txt 
```
To obtain the comments, first create two folders in the same directory with name example: Comments and NewsComments
The python command to download comments will be :
```
 python DownloadYouTubeComments c VideoIDs.txt Comments Key.txt
```
```
python DownloadYouTubeComments c VideoIDs1.txt NewsComments Key.txt 
```
To obtain parsed comments, create 2 directories at the directory structure level as Comments and NewsComments example: CommentsParsed and NewsCommentsParsed
Then use the following commands: 
```
python ParseComments Comments CommentsParsed
```
```
python ParseComments NewsComments NewsCommentsParsed
```
### Convert and Merge:
We can run CapstonConvertandMerge.py to convert the jsonbyline files in CommentsParsed and NewsCommentsParsed and same them in either .json or .csv format.
## Language Identification with IndicLID

### Overview
This project uses the IndicLID model from AI4Bharat to perform language identification on a dataset of text data extracted from JSON files. The model can detect multiple Indian languages and is designed to process and predict language distributions in given texts. 

You can learn more about the model here: [https://github.com/AI4Bharat/IndicLID/tree/master](url)

### Prerequisites
- Python 3.6 or later
- fasttext
- transformers

### Installation Instructions

#### Clone the Repository
First, clone this repository and navigate to the project directory:
```
git clone https://github.com/AI4Bharat/IndicLID.git
cd IndicLID/Inference
```
#### Create and Navigate to the Models Directory
```
mkdir models
cd models
```
#### Download Model Files
#### Download the necessary model files using wget:
```
wget https://github.com/AI4Bharat/IndicLID/releases/download/v1.0/indiclid-bert.zip
wget https://github.com/AI4Bharat/IndicLID/releases/download/v1.0/indiclid-ftn.zip
wget https://github.com/AI4Bharat/IndicLID/releases/download/v1.0/indiclid-ftr.zip
```

#### Unzip the downloaded model archives:
```
unzip indiclid-bert.zip
unzip indiclid-ftn.zip
unzip indiclid-ftr.zip
```

#### Initialize the IndicLID Model
#### Initialize the model with specified thresholds for input and roman language identification:
```
from ai4bharat.IndicLID import IndicLID
IndicLID_model = IndicLID(input_threshold = 0.5, roman_lid_threshold = 0.6)
```
#### Load and Process Data
#### Ensure your data is in JSON format and placed in the appropriate directory. Update the script to point to the correct file location:

```
file_path = 'IdentificationModel/Reddit/MergedDelhi.json'
```

#### Run the script to perform language identification on your data:
```
python IdentificationModel/Reddit/Identifyfinal.ipynb
```

#### Interface
<!-- colab integratation on running the model on custom input python script -->
Inference Notebook --> [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/12BZWviNtrxdtKEh8TVFTgCFVSgwb3JhD?usp=sharing)

#### Data Handling

The script includes functions to extract text bodies from comments and their replies in JSON files, clean them, and prepare them for language identification.

#### Testing

Tests are included to ensure the data is read correctly and the model predictions are functioning as expected.

#### Output

The script outputs the language prediction for each unique text string found in the dataset and prints the total count of processed texts.

### YouTube Comments:
Upload AllComments.csv to [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1D7uu7-qOmiVhFhWaSSydAGR08hwm5D7Y?usp=sharing) for language identification. Download LanguageIdentifiedComments.csv and save it in the dsci601project directory

# Data Exploration and Visualization

## Reddit

Once you have run the model for identifaction you can start data exploration by following the script in DataExploration/Reddit/DataExploration.ipynb 

#### Interface
<!-- colab integratation on running the model on custom input python script -->
Inference Notebook --> [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/162cDyVFB6P0xEA3rIZQGMdWhjdEsvmN4?usp=sharing)

## YouTube
Upload LanguageIdentifiedComments.csv to [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1YgFmB9Dd9juPvp4dYviYfdoRmVS1V5mL?usp=sharing) for data exploration

#### Testing
A test is included in this notebook [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1t3dEf6dyq6TuKY7QmSln0j4fKnM712V0?usp=sharing) to ensure that the comments are processed correctly 







 

 

