import requests 
import json

import os 
from dotenv import load_dotenv

load_dotenv(dotenv_path="./.env")

API_KEY = os.getenv("API_KEY")
CHANNEL_HANDLE = "mkbhd"
maxResults = 50


def get_playlist_id():

    try:
        url = f'https://youtube.googleapis.com/youtube/v3/channels?part=contentDetails&forHandle={CHANNEL_HANDLE}&key={API_KEY}'

        response = requests.get(url)

        response.raise_for_status()

        # print(response)

        data = response.json()

        json.dumps(data, indent=4)

        # print(json.dumps(data, indent=4))

        channel_items = data["items"][0]

        channel_playlistID = channel_items["contentDetails"]["relatedPlaylists"]["uploads"]

        # print(channel_playlistID)

        return channel_playlistID
    
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while fetching the playlist ID: {e}")
        return None
    


    
def get_video_ids(playlistId):

    video_ids = [] 

    pageToken = None 

    base_url =   f"https://youtube.googleapis.com/youtube/v3/playlistItems?part=contentDetails&maxResults={maxResults}&playlistId={playlistId}&key={API_KEY}"

    try: 

        while True: 

            url = base_url 

            # Get the first page of results, then subsequent pages using the pageToken
            if pageToken: 
                url += f"&pageToken={pageToken}"

            response = requests.get(url)

            response.raise_for_status()

            data = response.json()

            for item in data.get("items", []):
                video_id = item["contentDetails"]["videoId"]
                video_ids.append(video_id) 

            pageToken = data.get("nextPageToken")

            if not pageToken: 
                break 

        return video_ids

    except requests.exceptions.RequestException as e:
        print(f"An error occurred while fetching video IDs: {e}")
        return None

if __name__ == "__main__":
    playlistId = get_playlist_id()
    get_video_ids(playlistId)
    





