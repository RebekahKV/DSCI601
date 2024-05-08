import os
import json
import pandas as pd
from typing import List

def read_json(folder_paths: List[str]) -> List[dict]:
    """
    Reads JSON files from the specified folder paths and returns a list of dictionaries.

    Args:
        folder_paths (List[str]): A list of paths to folders containing JSON files.

    Returns:
        List[dict]: A list of dictionaries containing data from the JSON files.
    """
    data = []
    for folder_path in folder_paths:
        for filename in os.listdir(folder_path):
            if filename.endswith("_jsonbyline.txt"):
                filepath = os.path.join(folder_path, filename)
                with open(filepath, "r") as file:
                    jsonFile = file.readlines()
                    for line in jsonFile:
                        data.append(json.loads(line))
    return data

def main() -> None:
    """Main function to read JSON files, convert them to DataFrame, and save as CSV and JSON files."""
    folder_paths = ["/Users/valerie/capstone/CodeForMadhav/CommentsParsed/jsonbyline",
                     "/Users/valerie/capstone/CodeForMadhav/NewsCommentsParsed/jsonbyline"]  # Add paths to all folders here
    data = read_json(folder_paths)

    df = pd.DataFrame(data)  # stores the data list in a dataframe

    print(df.head())

    # download this file to .json
    df.to_json('Comments17262.json', index=False) 
     
    # download this file to .csv
    df.to_csv('Comments17262.csv', index=False) 

    print(df.describe())

if __name__ == "__main__":
    main()
