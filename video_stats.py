import requests 
import json
import os 

from datetime import date
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
    

def extract_video_data(video_ids):

    extracted_data = [] 

    def batch_list(video_id_list, batch_size = maxResults):
        for video_id in range (0, len(video_id_list), batch_size):
            yield video_id_list[video_id: video_id + batch_size]

    try: 
        for batch in batch_list(video_ids, maxResults):
            video_ids_str = ",".join(batch)

            url =   f'https://youtube.googleapis.com/youtube/v3/videos?part=contentDetails%20&part=snippet&part=statistics%20&id={video_ids_str}&key={API_KEY}'

            response = requests.get(url)

            response.raise_for_status()

            data = response.json()

            for item in data.get("items", []):
                video_id = item["id"]
                snippet = item["snippet"]
                statistics = item["statistics"]
                contentDetails = item["contentDetails"]

                video_data = {
                    "video_id": video_id,
                    "title": snippet["title"],
                    "PublishedAt": snippet["publishedAt"],
                    "duration": contentDetails["duration"],
                    "viewCount": statistics.get("viewCount",None),
                    "likeCount": statistics.get("likeCount",None),
                    "commentCount": statistics.get("commentCount", None),
                }

                extracted_data.append(video_data)

        return extracted_data
    
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while fetching video data: {e}")
        return None

def save_to_json(extracted_data):
    file_path = f"./data/video_data_{date.today()}.json"

    with open(file_path, "w", encoding="utf-8") as json_file:
        json.dump(extracted_data, json_file, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    playlistId = get_playlist_id()
    video_ids = get_video_ids(playlistId)
    video_data = extract_video_data(video_ids)
    save_to_json(video_data)
     





