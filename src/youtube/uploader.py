import os
import json
import google.oauth2.credentials
import google_auth_oauthlib.flow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.auth.transport.requests import Request

# This scope allows for full access to the user's YouTube account.
SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]
API_SERVICE_NAME = "youtube"
API_VERSION = "v3"

class YouTubeUploader:
    def __init__(self, config_path='config.json'):
        with open(config_path) as f:
            config = json.load(f)

        youtube_config = config.get('youtube', {})
        self.client_secret_file = youtube_config.get('client_secret_file')
        self.credentials_file = 'youtube_credentials.json'

    def get_authenticated_service(self):
        credentials = None
        if os.path.exists(self.credentials_file):
            credentials = google.oauth2.credentials.Credentials.from_authorized_user_file(self.credentials_file, SCOPES)

        if not credentials or not credentials.valid:
            if credentials and credentials.expired and credentials.refresh_token:
                credentials.refresh(Request())
            else:
                if not self.client_secret_file or not os.path.exists(self.client_secret_file):
                    print("Error: YouTube client secret file not found. Please configure it in config.json.")
                    return None

                flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(self.client_secret_file, SCOPES)
                credentials = flow.run_console() # Changed from run_local_server to be more friendly for terminal-based apps

            with open(self.credentials_file, 'w') as f:
                f.write(credentials.to_json())

        return build(API_SERVICE_NAME, API_VERSION, credentials=credentials)

    def upload_video(self, video_path, title, description, tags):
        youtube = self.get_authenticated_service()
        if not youtube:
            print("Could not get authenticated YouTube service. Aborting upload.")
            return

        body = {
            'snippet': {
                'title': title,
                'description': description,
                'tags': tags,
                'categoryId': '24' # Entertainment
            },
            'status': {
                'privacyStatus': 'private' # 'private', 'public', or 'unlisted'
            }
        }

        try:
            print(f"Uploading video: {video_path}")
            insert_request = youtube.videos().insert(
                part=','.join(body.keys()),
                body=body,
                media_body=video_path
            )

            response = insert_request.execute()
            print(f"Video uploaded successfully! Video ID: {response['id']}")
            return response['id']
        except HttpError as e:
            print(f"An HTTP error {e.resp.status} occurred: {e.content}")
            return None
        except Exception as e:
            print(f"An error occurred during upload: {e}")
            return None

if __name__ == '__main__':
    # Example usage:
    # 1. Make sure your 'config.json' points to your client_secret.json
    # 2. Run this script once to authorize.
    # 3. Then you can call the upload_video method.
    uploader = YouTubeUploader()
    # You would call it like this:
    # uploader.upload_video("final_video.mp4", "My Awesome Compilation", "A video of cool stuff.", ["compilation", "memes"])
    print("YouTube Uploader module loaded. Run from main.py to upload a video.")
    # Test authentication
    service = uploader.get_authenticated_service()
    if service:
        print("Successfully authenticated with YouTube.")
    else:
        print("Failed to authenticate with YouTube.")