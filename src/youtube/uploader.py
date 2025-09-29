import os
import json
import google.oauth2.credentials
import google_auth_oauthlib.flow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.auth.transport.requests import Request
from src.logger import log

# This scope allows for full access to the user's YouTube account.
SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]
API_SERVICE_NAME = "youtube"
API_VERSION = "v3"

class YouTubeUploader:
    def __init__(self, config_path='config.json'):
        with open(config_path) as f:
            config = json.load(f)

        youtube_config = config.get('youtube', {})
        # Prepend the credentials directory to the file paths
        self.credentials_dir = 'credentials'
        client_secret_filename = youtube_config.get('client_secret_file', 'client_secret.json')
        self.client_secret_file = os.path.join(self.credentials_dir, client_secret_filename)
        self.credentials_file = os.path.join(self.credentials_dir, 'youtube_credentials.json')

    def get_authenticated_service(self):
        credentials = None
        if os.path.exists(self.credentials_file):
            credentials = google.oauth2.credentials.Credentials.from_authorized_user_file(self.credentials_file, SCOPES)
            log.info("Loaded YouTube credentials from file.")

        if not credentials or not credentials.valid:
            if credentials and credentials.expired and credentials.refresh_token:
                log.info("Refreshing expired YouTube credentials.")
                credentials.refresh(Request())
            else:
                if not os.path.exists(self.client_secret_file):
                    log.error(f"YouTube client secret file not found at '{self.client_secret_file}'.")
                    log.error("Please ensure it exists and is configured correctly.")
                    return None

                log.info("Performing first-time YouTube authentication.")
                log.info("Please follow the link provided in the console to authorize the application.")
                flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(self.client_secret_file, SCOPES)
                credentials = flow.run_local_server(open_browser=False)

            # Ensure the credentials directory exists before writing the file
            os.makedirs(self.credentials_dir, exist_ok=True)
            with open(self.credentials_file, 'w') as f:
                f.write(credentials.to_json())
            log.info(f"Saved new YouTube credentials to '{self.credentials_file}'.")

        return build(API_SERVICE_NAME, API_VERSION, credentials=credentials)

    def upload_video(self, video_path, title, description, tags):
        youtube = self.get_authenticated_service()
        if not youtube:
            log.error("Could not get authenticated YouTube service. Aborting upload.")
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
            log.info(f"Uploading video '{video_path}' to YouTube...")
            insert_request = youtube.videos().insert(
                part=','.join(body.keys()),
                body=body,
                media_body=video_path
            )

            response = insert_request.execute()
            log.info(f"Video uploaded successfully! Video ID: {response['id']}")
            return response['id']
        except HttpError as e:
            log.error(f"An HTTP error {e.resp.status} occurred during upload: {e.content}")
            return None
        except Exception as e:
            log.error(f"An unexpected error occurred during upload: {e}")
            return None

if __name__ == '__main__':
    # This is for testing the uploader directly.
    log.info("Testing YouTubeUploader module...")
    uploader = YouTubeUploader()
    service = uploader.get_authenticated_service()
    if service:
        log.info("Successfully authenticated with YouTube.")
    else:
        log.error("Failed to authenticate with YouTube.")