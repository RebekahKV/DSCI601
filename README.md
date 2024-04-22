# DSCI601
## Data Collection
## Reddit data:
Reddit Data Retrieval Using PRAW

### Overview
This project utilizes the Python Reddit API Wrapper (PRAW) to scrape Reddit posts and comments based on specific keywords within certain subreddits. The data is then saved in JSON format. This script is designed to to gather discussions from various dates and subreddits.

### Prerequisites
- Python 3.6 or later
- pip (Python package installer)

### Installation Instructions

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
python script_name.py  
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

To Extract video IDs only use the Google Colab Notebook CapstoneExtractVideoIds.ipynb [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1IOXp0ewtgjOcPMmGGz_cPA_L7uf0HPJj?usp=sharing)
Generate "VideoIDs.txt" and "VideoIDs1.txt"

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
### Convert .json to .csv:
In CommentsParsed and NewsCommentsParsed: compress the jsonbyline file to jsonbyline.zip
Upload the CommentsParsed jsonbyline.zip to [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/132CjI7gdlrL30vhY6PzGVIS4iP5LdGZZ?usp=sharing) and then download the Comments.csv file into the dsci601project directory
Upload the NewsCommentsParsed jsonbyline.zip to [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1CSHCrr8YyOAbMUCA3WKRM1DNkgCU547I?usp=sharing) and then download the NEWSComments.csv file into the same directory




 

