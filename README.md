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
