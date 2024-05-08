################################################################################
#                                                                              #
################################################################################
"""
Install the 'praw' library using pip.

The 'praw' library is a Python wrapper for the Reddit API, allowing you to easily
access data from the Reddit platform.
"""

!pip install praw --quiet

################################################################################
#                                                                              #
################################################################################
"""
Import required libraries for the script.

This code imports the following libraries:

- `praw`: A Python wrapper for the Reddit API, allowing you to easily access data from the Reddit platform.
- `pandas`: A data manipulation library that provides easy-to-use data structures and data analysis tools.
- `json`: A built-in Python library that provides functions for working with JSON data, which is a lightweight
          data interchange format commonly used in web APIs.
"""

import praw
import pandas as pd
import json

################################################################################
#                                                                              #
################################################################################
"""
Run the 'secrets.py' script that contains Reddit API tokens.

This code runs the 'secrets.py' script that contains confidential information such as
secret keys, passwords, and API tokens. The script loads the confidential information into
the notebook environment, allowing you to access the API without exposing your credentials.

After running this code cell, the 'secrets.py' file will be deleted from the system to avoid
exposing confidential information.
"""

%run secrets.py
# !rm secrets.py

################################################################################
#                                                                              #
################################################################################
"""
Initialize a 'praw' Reddit API instance with authentication parameters.

`praw.Reddit` initializes an instance of the `praw` Reddit API with your account
credentials, allowing you to interact with the Reddit platform. The following
parameters are required to authenticate your account:

- `client_id`: Your Reddit application client ID, obtained by registering a new
               app on the Reddit website.
- `client_secret`: Your Reddit application client secret, obtained by registering
                   a new app on the Reddit website.
- `username`: Your Reddit account username.
- `password`: Your Reddit account password.
- `user_agent`: A string that identifies your Reddit application to the Reddit API.
                It should be unique and descriptive, and follow the format
                "platform:app_id:version (by /u/username)".

Note: The values of the authentication parameters should be replaced with your own
credentials for the script to function correctly.
"""


reddit_instance = praw.Reddit(client_id = CLIENT_ID, #peronal use script
                    client_secret = CLIENT_SECRET, #secret token
                    username = REDDIT_USERNAME, #profile username
                    password = REDDIT_PASSWORD, #profile password
                    user_agent = "USERAGENT")

################################################################################
#                                                                              #
################################################################################
"""
Initialize empty lists for storing Reddit post attributes.

This code initializes empty lists for storing various attributes of Reddit posts, such as
titles, selftext, scores, authors, creation timestamps, subreddits, number of comments,
permalinks, and upvote ratios. These lists can be used to store the corresponding attributes
of multiple Reddit posts and analyze them collectively.

@var title_list: An empty list for storing the titles of Reddit posts.
@var selftext_list: An empty list for storing the selftext of Reddit posts.
@var score_list: An empty list for storing the scores of Reddit posts.
@var author_list: An empty list for storing the authors of Reddit posts.
@var created_utc_list: An empty list for storing the creation timestamps of Reddit posts in UTC.
@var subreddit_list: An empty list for storing the subreddits of Reddit posts.
@var num_comments_list: An empty list for storing the number of comments of Reddit posts.
@var permalink_list: An empty list for storing the permalinks of Reddit posts.
@var upvote_ratio_list: An empty list for storing the upvote ratios of Reddit posts.
"""
title_list = []
selftext_list = []
score_list = []
author_list = []
created_utc_list = []
subreddit_list = []
num_comments_list = []
permalink_list = []
upvote_ratio_list = []

################################################################################
#                                                                              #
################################################################################
"""
Initialize a list of subreddit names.

This code initializes a list of subreddit names that will be used to fetch data
from the Reddit platform. The list contains the following subreddit names:

- 'guncontrol': A subreddit dedicated to discussions about gun control policies.
- 'GunsAreCool': A subreddit that advocates for gun control and provides news and commentary on gun violence.
- 'progun': A subreddit that supports gun rights and provides news and commentary on gun-related issues.
- '2ALiberals': A subreddit for liberal gun owners to discuss gun-related issues.
- 'GunViolence': A subreddit that focuses on news and discussions related to gun violence in the United States.
- 'MassShooting': A subreddit that tracks mass shooting incidents in the United States.

@param subreddit_names: A list of subreddit names.
@type subreddit_names: list
"""

subreddit_names = ['Delhi']

################################################################################
#                                                                              #
################################################################################
count = 0
import datetime
import time
def scrape_reddit_data(subreddit_name, reddit):
    global count
    """
    Scrapes comments and posts from the specified subreddits and returns the collected data,
    filtering for posts from January 2024.

    @param subreddit_name: A list of subreddit names to scrape.
    @type subreddit_name: list

    @return: A list of dictionaries containing information about the posts and their comments.
    @rtype: list
    """

    data = []
    keywords = ['punjab', 'farmer', 'stubble']
    query = ' OR '.join(keywords)

    # Define start and end dates
    start_date = datetime.datetime(2019, 1, 1)
    end_date = datetime.datetime(2023, 4, 20)

    # Create a subreddit object using the specified name
    subreddit = reddit.subreddit(subreddit_name)

    # Retrieve submissions from the subreddit using search
    posts = subreddit.search(query, limit=None)

    # Loop through each submission in the subreddit post
    for post in posts:
        # Convert post creation time from UTC to a datetime object
        post_date = datetime.datetime.utcfromtimestamp(post.created_utc)

        # Filter posts to include only those from January 2024
        if start_date <= post_date < end_date:
            post.comments.replace_more(limit=None)
            comments_list = []

            # Loop through each comment in each post
            for comment in post.comments:
                reply_list = []
                # Loop through each reply to the comment
                for reply in comment.replies:
                    reply_list.append({
                        'body': reply.body,
                        'score': reply.score,
                        'created_utc': reply.created_utc,
                        'author': reply.author.name if reply.author else '[deleted]',
                        'id': reply.id,
                        'is_submitter': reply.is_submitter,
                        'parent_id': reply.parent_id
                    })
                    time.sleep(0.1)
                comments_list.append({
                    'body': comment.body,
                    'score': comment.score,
                    'created_utc': comment.created_utc,
                    'reply': reply_list,
                    'author': comment.author.name if comment.author else '[deleted]',
                    'id': comment.id,
                    'is_submitter': comment.is_submitter,
                    'parent_id': comment.parent_id
                })
                time.sleep(0.1)
            data.append({
                'author': post.author.name if post.author else '[deleted]',
                'subreddit': post.subreddit.display_name,
                'title': post.title,
                'selftext': post.selftext,
                'score': post.score,
                'created_utc': post.created_utc,
                'permalink': post.permalink,
                'upvote_ratio': post.upvote_ratio,
                'num_comments': post.num_comments,
                'comments': comments_list,
                'id': post.id
            })
        time.sleep(0.1)
        count += 1
        print(count)
    return data

################################################################################
#                                                                              #
################################################################################
def save_reddit_data_to_file(data, filename):
    """
    Saves the scraped data to a JSON file with the specified filename.

    :param data: The data to be saved.
    :type data: list

    :param filename: The name of the file to save the data to.
    :type filename: str

    :return: None
    """
    with open(filename, 'w') as f:
        json.dump(data, f)

################################################################################
#                                                                              #
################################################################################
# Loop through each subreddit name in the list
for each_subreddit in subreddit_names:
  # Call the scrape_reddit_data function to collect data from the specified subreddits using the Reddit instance
  data = scrape_reddit_data(each_subreddit,reddit_instance)
  # Save the scraped data to a JSON file named 'reddit_dataset.json'
  save_reddit_data_to_file(data, each_subreddit+'.json')

################################################################################
#                                                                              #
################################################################################


