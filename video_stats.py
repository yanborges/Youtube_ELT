import requests 
import json

import os 
from dotenv import load_dotenv

load_dotenv(dotenv_path="./.env")

API_KEY = os.getenv("API_KEY")

CHANNEL_HANDLE = "mkbhd"

def get_playlist_id():

    try:
        url = f'https://youtube.googleapis.com/youtube/v3/channels?part=contentDetails&forHandle={CHANNEL_HANDLE}&key={API_KEY}'

        response = requests.get(url)

        # print(response)

        data = response.json()

        json.dumps(data, indent=4)

        # print(json.dumps(data, indent=4))

        channel_items = data["items"][0]

        channel_playlistID = channel_items["contentDetails"]["relatedPlaylists"]["uploads"]

        print(channel_playlistID)

        return channel_playlistID
    
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while fetching the playlist ID: {e}")
        return None
    
if __name__ == "__main__":
    get_playlist_id()




