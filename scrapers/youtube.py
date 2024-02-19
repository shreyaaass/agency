from youtube_transcript_api import YouTubeTranscriptApi
import requests

def get_video_details(api_key, video_id):
    base_url = "https://www.googleapis.com/youtube/v3/videos"
    params = {
        'id': video_id,
        'part': 'snippet,contentDetails,statistics',
        'key': api_key,
    }
    transcript=getTranscript(video_id)
    response = requests.get(base_url, params=params)
    # print(response.content)
    if response.status_code == 200:
        video_data = response.json()
        title = video_data['items'][0]['snippet']['title'].replace("\n","")
        description = video_data['items'][0]['snippet']['description'].replace("\r"," ").replace("\n"," ")
        views = video_data['items'][0]['statistics']['viewCount']

        print(f"{title};{description};{views};{transcript}")
    else:
        print(f"Error {response.status_code}: {response.text}")



def getTranscript(videoId):
    transcript=[i["text"].strip("'") for i in YouTubeTranscriptApi.get_transcript(videoId)]
    return(" ".join(transcript).replace("\n",""))
    
api_key = 'AIzaSyAJOJf7ePjrXyFLO6nX4C-L-CiSDNiuuoU'


with open("videoId.txt", "r") as file:
    for video_id in file:
        try:
            get_video_details(api_key,video_id.strip())
        except:
            pass