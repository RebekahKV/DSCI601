"""
Code provided by Prof. Ashiqur R. KhudaBukhsh
"""

import json 
import os, sys
import pprint 
import pandas as pd 
#import matplotlib.pyplot as plt 
import datetime



if __name__ == '__main__' :
    """
    Example Usage : 

    python parse_comments.py comment_directory comment_root_name 

    comment_directory : Where the comments are saved 
    comment_root_name : where the csv and jsobbyline are saved


    Notes : 
    1. comment_directory must be a folder 
    2. comment_root_name : /path/to/comments  DONT END WITH A SLASH
 
    """
    
    comment_directory = sys.argv[1]
    comment_root_name = sys.argv[2]
    total_comments_found = 0
    
    if not os.path.isdir(comment_root_name):
        os.makedirs(comment_root_name)
        print("Creating save directory")

    comment_root_name_metadata = os.path.join(comment_root_name, "metadata")
    comment_root_name_jsonbyline = os.path.join(comment_root_name, "jsonbyline")

    if not os.path.exists(comment_root_name_metadata):
        os.makedirs(comment_root_name_metadata)

    if not os.path.exists(comment_root_name_jsonbyline): 
        os.makedirs(comment_root_name_jsonbyline)
    
    print("Creating save subdirectories")

    total_videos = len(os.listdir(comment_directory))

    for video_name in os.listdir(comment_directory):
        tlc_properties = {}                          # save comment metadata
        comments_byline = {}                         # save only id and comment 

        filepath = os.path.join("{}/{}/".format(comment_directory, video_name))
        #print(filepath)
        pages = os.listdir(filepath)
        for page in pages:
            with open("{}/{}/{}".format(comment_directory, video_name,page), 'r', encoding='utf-8') as file:
                #f = file.read().encode('ascii', 'ignore')
                data = json.load(file)
                for item in data["items"]:
                    snip = item['snippet']['topLevelComment']['snippet']
                    unique_id = snip["authorChannelUrl"].split("/")[-1]
                    # this is one top level comment - 
                    tlc_properties[item["id"]] = [item["snippet"]["videoId"],
                                                unique_id, 
                                                snip["authorChannelUrl"].split("/")[-1],
                                                item['snippet']['topLevelComment']['snippet']['authorDisplayName'],
                                                item["snippet"]["topLevelComment"]["snippet"]["likeCount"],
                                                item["snippet"]["topLevelComment"]["snippet"]["publishedAt"],
                                                item["snippet"]["topLevelComment"]["snippet"]["updatedAt"],
                                                item["snippet"]["totalReplyCount"],
                                                item["snippet"]["isPublic"]
                                                ]
                    
                    comments_byline[item["id"]] = {
                            "commentId" : "{0}".format(item["id"]),
                            "text": "{0}".format(item["snippet"]["topLevelComment"]["snippet"]["textDisplay"])
                        }
            
        
        df = pd.DataFrame.from_dict(tlc_properties, orient = "index",
                            columns = ["videoId","uniqueAuthorId","authorChannelUrl","author","likeCount","publishedAt","updatedAt","totalReplyCount","isPublic"])

        df.reset_index(drop=False, inplace=True)
        df.rename(columns={"index" : "commentId" }, inplace = True)

        print(f"Found {df.shape[0]} comments from video ID {video_name}")  
        total_comments_found = total_comments_found + df.shape[0]  
    

        file_name = sys.argv[1].split("/")[-1]

        comment_datapath = f"{comment_root_name_metadata}/{video_name}_metadata.csv" 
        comment_jsonbyline = f"{comment_root_name_jsonbyline}/{video_name}_jsonbyline.txt" 

        print(f"Writing comment mdetadata to {comment_datapath}")
        df.to_csv(comment_datapath, index=False)

        print(f"Writing jsonbyline to {comment_jsonbyline}")
        with open(comment_jsonbyline, "w") as fp1:
            for key, value in comments_byline.items():
                fp1.write(json.dumps(value))
                fp1.write("\n")


    print(f"Found {total_comments_found} comments from video ID")  


