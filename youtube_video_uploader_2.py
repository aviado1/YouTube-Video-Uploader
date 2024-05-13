import os
import pickle
import datetime
import time
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload

# Define constants with generic placeholders
SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]
API_SERVICE_NAME = "youtube"
API_VERSION = "v3"
CLIENT_SECRETS_FILE = "YOUR_CLIENT_SECRET_FILE.json"  # Replace with the path to your client secrets file.
TOKEN_FILE = "token.pickle"
VIDEO_DIR = "PATH_TO_YOUR_VIDEO_DIRECTORY"  # Replace with the path to your video directory.

def authenticate_youtube():
    """Authenticate to YouTube API and return the service object."""
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
    print("Authenticating to YouTube API...")
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, "rb") as token:
            credentials = pickle.load(token)
    else:
        flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
        credentials = flow.run_local_server(port=0)
        with open(TOKEN_FILE, "wb") as token:
            pickle.dump(credentials, token)
    return build(API_SERVICE_NAME, API_VERSION, credentials=credentials)

def get_file_creation_date(file_path):
    """Retrieve the file's creation date and return it formatted as DD/MM/YYYY."""
    timestamp = os.path.getmtime(file_path)
    return datetime.datetime.fromtimestamp(timestamp).strftime('%d/%m/%Y')

def upload_video(youtube, file_path):
    """Uploads a video file to YouTube with quota management and countdown timer."""
    video_date = get_file_creation_date(file_path)
    video_title = f"GoPro Video {video_date}"
    request_body = {
        'snippet': {
            'categoryId': '22',
            'title': video_title,
            'description': f'Uploaded on {video_date} by automated script',
            'tags': ['GoPro', 'auto upload']
        },
        'status': {
            'privacyStatus': 'private'
        }
    }

    media_file = MediaFileUpload(file_path, mimetype='video/*', resumable=True)

    try:
        print(f"Uploading {os.path.basename(file_path)}...")
        response = youtube.videos().insert(
            part="snippet,status",
            body=request_body,
            media_body=media_file
        ).execute()
        print(f'Successfully uploaded video ID: {response.get("id")}')
    except HttpError as error:
        print(f"An HTTP error {error.resp.status} occurred: {error.content}")
        if error.resp.status == 403 and 'quotaExceeded' in str(error):
            pause_duration = 3600  # 1 hour
            print("Quota exceeded. Pausing uploads...")
            for i in range(pause_duration, 0, -1):
                time_left = f"{i//3600:02}:{(i%3600)//60:02}:{i%60:02}"
                print(f"Resuming in {time_left}", end='\r')
                time.sleep(1)
            print("\nResuming uploads now...")

def main():
    """Main function to handle video upload process."""
    youtube = authenticate_youtube()
    videos = os.listdir(VIDEO_DIR)
    total_videos = len(videos)
    print(f"Found {total_videos} videos in directory.")

    for i, filename in enumerate(videos, 1):
        if filename.lower().endswith(('.mp4', '.mov')):
            file_path = os.path.join(VIDEO_DIR, filename)
            print(f"Processing video {i} of {total_videos}: {filename}")
            upload_video(youtube, file_path)
            time.sleep(1)  # Wait for 1 second to respect the Queries per minute limit

if __name__ == "__main__":
    main()
