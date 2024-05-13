import os
import pickle
import datetime
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload

# Define constants
SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]
API_SERVICE_NAME = "youtube"
API_VERSION = "v3"
CLIENT_SECRETS_FILE = "PATH_TO_YOUR_CLIENT_SECRET_FILE.json"  # Replace with the path to your client secrets file.
TOKEN_FILE = "token.pickle"
VIDEO_DIR = "PATH_TO_YOUR_VIDEO_DIRECTORY"  # Replace with the path to your video directory.

def authenticate_youtube():
    """
    Authenticate to YouTube API and return the service object.
    This function handles OAuth2 authentication and token storage/retrieval.
    """
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"
    
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
    """
    Retrieve the file's creation date and return it formatted as DD/MM/YYYY.
    This is used to generate video titles based on the date the video was recorded.
    """
    timestamp = os.path.getmtime(file_path)
    return datetime.datetime.fromtimestamp(timestamp).strftime('%d/%m/%Y')

def upload_video(youtube, file_path):
    """
    Uploads a video file to YouTube.
    The video title is set to "GoPro Video {video date}", and the video is uploaded as private.
    """
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
        response = youtube.videos().insert(
            part="snippet,status",
            body=request_body,
            media_body=media_file
        ).execute()
        print(f'Uploaded video ID: {response.get("id")}')
    except HttpError as error:
        print(f"An HTTP error {error.resp.status} occurred: {error.content}")

def main():
    """
    Main function to handle the video upload process.
    Iterates through all video files in the specified directory and uploads them to YouTube.
    """
    youtube = authenticate_youtube()
    for filename in os.listdir(VIDEO_DIR):
        if filename.lower().endswith(('.mp4', '.mov')):
            file_path = os.path.join(VIDEO_DIR, filename)
            upload_video(youtube, file_path)
            print(f"Uploaded: {filename}")

if __name__ == "__main__":
    main()
