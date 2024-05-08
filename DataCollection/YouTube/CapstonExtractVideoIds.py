from typing import List, Optional
import pandas as pd
import re

def extractVideoIDs(data: pd.DataFrame, column: str) -> List[Optional[str]]:
    """
    Extracts video IDs from a DataFrame column.

    Args:
        data (pd.DataFrame): The DataFrame containing the data.
        column (str): The name of the column containing video URLs.

    Returns:
        List[Optional[str]]: A list of video IDs extracted from the URLs.
    """
    pattern = r'(?<=watch\?v=)[^&]+'
    videoIDs = [re.search(pattern, url).group(0) if re.search(pattern, url) else None for url in data[column]]
    return videoIDs

def saveVideoIds(videoIDs: List[Optional[str]], file_name: str) -> None:
    """
    Saves video IDs to a text file.

    Args:
        videoIDs (List[Optional[str]]): A list of video IDs to be saved.
        file_name (str): The name of the text file to save the video IDs.
    """
    with open(file_name, 'w') as file:
        for videoID in videoIDs:
            if videoID:
                file.write(videoID + '\n')

# Load AirPollutionVideos.csv
dfSQ1 = pd.read_csv('/Users/valerie/capstone/CodeForMadhav/AirPollutionVideos.csv')

# Extract video IDs from AirPollutionVideos.csv and save them to VideoIDs.txt
videoIds = extractVideoIDs(dfSQ1, 'Video')
# Change file path to save video IDs in a specific directory
saveVideoIds(videoIds, 'VideoIDs123.txt') 

# Load AirPollutionNews.csv
dfSQ2 = pd.read_csv('/Users/valerie/capstone/CodeForMadhav/AirPollutionNEWS.CSV')

# Extract video IDs from AirPollutionNews.csv and save them to VideoIDs1.txt
videoIds1 = extractVideoIDs(dfSQ2, 'VideoURL')
# Change file path to save video IDs in a specific directory
saveVideoIds(videoIds1, 'VideoIDs1345.txt')
