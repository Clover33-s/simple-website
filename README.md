# Content Grinder - Automated YouTube Bot

Content Grinder is a Python-based bot that automates the process of creating and publishing video compilations to YouTube. It scrapes media from various online sources, compiles them into a single video, and uploads it to a specified YouTube channel.

## Features

- **Functional Reddit Scraper**: Includes a working scraper for fetching media from Reddit.
- **Extensible Scraper Architecture**: The project is designed to be extended with new scrapers for other platforms.
- **Automated Video Compilation**: Automatically downloads media and compiles it into a single video file using MoviePy.
- **Direct YouTube Upload**: Uploads the final video directly to your YouTube channel using the YouTube Data API v3 and OAuth 2.0.
- **Customizable Configuration**: A simple `config.json` file to manage all your settings.

**NOTE on Other Platforms (TikTok, Twitter, etc.)**: This project includes a *non-functional placeholder* for a TikTok scraper to demonstrate its extensible design. Scraping modern, Javascript-heavy platforms like TikTok is a complex and volatile task that typically requires using unofficial, reverse-engineered API libraries which can be unstable and require frequent updates. A similar approach would be needed to implement a scraper for Twitter.

## Installation and Setup

### Step 1: Clone the Repository

```bash
git clone <repository_url>
cd <repository_directory>
```

### Step 2: Configure Credentials

This application requires API credentials for both Reddit and YouTube. All credential files must be placed inside the `credentials/` directory.

#### A. Reddit API Credentials

1.  Navigate to the `credentials/` directory.
2.  Rename `praw.ini.example` to `praw.ini`.
3.  Follow the instructions in the [PRAW documentation](https://praw.readthedocs.io/en/latest/getting_started/authentication.html) to get your API credentials for a "script" application.
4.  Fill in your details in `credentials/praw.ini`. The `user_agent` must be a unique and descriptive string.

    ```ini
    # credentials/praw.ini
    [bot1]
    client_id=YOUR_CLIENT_ID
    client_secret=YOUR_CLIENT_SECRET
    username=YOUR_REDDIT_USERNAME
    password=YOUR_REDDIT_PASSWORD
    user_agent=ContentGrinder bot by u/yourusername
    ```

#### B. YouTube API Credentials

1.  Follow the steps below to download your OAuth 2.0 client secrets file from the Google Cloud Console.
    1.  Go to the [Google Cloud Console](https://console.cloud.google.com/).
    2.  Create a new project.
    3.  Search for and enable the **YouTube Data API v3**.
    4.  From the navigation menu, go to **APIs & Services** -> **Credentials**.
    5.  Click **+ CREATE CREDENTIALS** and select **OAuth client ID**.
    6.  Choose **Desktop app** for the application type and give it a name.
    7.  Click **CREATE**. From the list of OAuth 2.0 Client IDs, find your newly created credential and click the **Download JSON** icon.
2.  Rename the downloaded file to `client_secret.json`.
3.  Move the `client_secret.json` file into the `credentials/` directory.

### Step 3: Choose Your Execution Method

You can run this application using Docker (recommended) or directly with Python.

---

### Option 1: Running with Docker (Recommended)

This method handles all Python and system dependencies for you.

**Prerequisites:**
- [Docker](https://www.docker.com/get-started) installed on your system.

**1. Build the Docker Image:**

From the project's root directory, run:
```bash
docker build -t content-grinder .
```

**2. Run the Docker Container:**

This command runs the bot and mounts your `credentials` directory into the container. This allows the application to use your API keys and, on the first run, save the YouTube authentication token back to your host machine.

```bash
docker run --rm -it -v "$(pwd)/credentials:/app/credentials" content-grinder
```

**First-time YouTube Authentication:** When you run the container for the first time, the application will pause and display a URL in your terminal. Copy this URL, paste it into your browser, and complete the authorization process. A `youtube_credentials.json` file will be created in your `credentials` directory, which will be used for all future runs.

---

### Option 2: Running Locally with Python

**Prerequisites:**
- Python 3.7+
- `pip` for package installation

**1. Install Dependencies:**

```bash
pip install -r requirements.txt
```

**2. Run the Bot:**

Make sure you have completed the credential setup in Step 2. Then, run the application:
```bash
python main.py
```

## How It Works

1.  **Scraping**: The bot reads the `config.json` to see which platforms are enabled and what to scrape.
2.  **Compilation**: The collected media (images and videos) are downloaded locally. The `VideoCompiler` uses `moviepy` to create a compilation. Images are converted into short video clips.
3.  **Uploading**: The final video is uploaded to YouTube using the credentials you provided.
4.  **Cleanup**: Temporary media files and the final compiled video are deleted from your local machine after a successful upload.