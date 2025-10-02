import os
import webbrowser
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

# This is the scope our application requires.
SCOPES = ['https://www.googleapis.com/auth/youtube.upload']
CLIENT_SECRETS_FILE = 'credentials/client_secret.json'
TOKEN_FILE = 'credentials/youtube_credentials.json'

def main():
    """
    This script performs a standalone YouTube authentication test.
    """
    print("--- YouTube Authentication Diagnostic Tool ---")

    creds = None
    # Check if we have already stored credentials.
    if os.path.exists(TOKEN_FILE):
        try:
            creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
            print(f"Loaded credentials from {TOKEN_FILE}")
        except Exception as e:
            print(f"Error loading credentials from {TOKEN_FILE}: {e}")
            print("Will attempt to re-authenticate.")
            creds = None

    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print("Credentials have expired. Refreshing...")
            try:
                creds.refresh(Request())
                print("Credentials refreshed successfully.")
            except Exception as e:
                print(f"Error refreshing credentials: {e}")
                print("Will attempt to re-authenticate from scratch.")
                creds = None

        if not creds:
            if not os.path.exists(CLIENT_SECRETS_FILE):
                print(f"ERROR: The client secrets file was not found at '{CLIENT_SECRETS_FILE}'.")
                print("Please ensure you have downloaded your credentials from Google Cloud and placed them correctly.")
                return

            print("No valid credentials found. Starting first-time authentication flow.")
            # The host='0.0.0.0' and port=8080 are set to match the Docker environment.
            # This will start a temporary web server to receive the auth token.
            try:
                flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
                # We use open_browser=False to prevent it from failing inside Docker.
                # The user will copy/paste the URL manually.
                auth_url, _ = flow.authorization_url(prompt='consent')

                print("\n--- ACTION REQUIRED ---")
                print("Please go to this URL in your browser to authorize the application:")
                print(f"\n{auth_url}\n")

                # In a real desktop app, you'd use flow.run_local_server().
                # For this diagnostic script, we will use the manual copy-paste method
                # as it is the most robust way to debug this specific issue.
                auth_code = input("After authorizing, you will be redirected. Copy the 'code' from the redirect URL and paste it here: ")

                flow.fetch_token(code=auth_code)
                creds = flow.credentials
                print("Successfully fetched token.")
            except Exception as e:
                print(f"\n--- AUTHENTICATION FAILED ---")
                print(f"An error occurred during the authentication flow: {e}")
                print("Please double-check your Google Cloud project settings, especially the 'Authorized redirect URIs'.")
                return

        # Save the credentials for the next run
        try:
            with open(TOKEN_FILE, 'w') as token:
                token.write(creds.to_json())
            print(f"Credentials saved successfully to {TOKEN_FILE}")
        except Exception as e:
            print(f"Error saving credentials: {e}")
    else:
        print("Credentials are valid.")

    print("\n--- DIAGNOSTIC COMPLETE ---")
    if creds and creds.valid:
        print("SUCCESS: Authentication test passed. Your credentials and setup are correct.")
        print("You can now try running the main application again.")
    else:
        print("FAILURE: Authentication test failed. Please review the error messages above.")

if __name__ == '__main__':
    main()