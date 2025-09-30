# AI Content Grinder - Automated YouTube Bot

Content Grinder is a fully autonomous Python-based bot that generates unique video content and publishes it to YouTube. It uses a Large Language Model (LLM) to brainstorm video ideas and a text-to-image model to create the visual content, which is then compiled into a video and uploaded.

## Features

- **Autonomous Idea Generation:** Uses a Large Language Model (e.g., GPT-4o mini) to generate creative and unique image prompts based on a user-defined theme.
- **AI Image Generation:** Leverages the Stability AI API to create high-quality images from the LLM-generated prompts.
- **Automated Video Compilation:** Automatically compiles the generated images into a video slideshow using MoviePy.
- **Direct YouTube Upload:** Uploads the final video directly to a specified YouTube channel using the YouTube Data API.
- **Fully Configurable:** A single `config.json` file manages all API keys, themes, and settings.
- **Docker Support:** Comes with a `Dockerfile` for easy, one-command setup and execution.

## How It Works

The bot operates in a fully autonomous, three-step pipeline:
1.  **Generate Ideas:** The bot connects to an LLM (like OpenAI's GPT) with a user-defined theme from `config.json`. The LLM returns a list of unique, detailed image prompts.
2.  **Generate Images:** These prompts are then sent to the Stability AI API, which generates a unique image for each prompt. The images are saved temporarily.
3.  **Compile and Upload:** The generated images are compiled into a video slideshow, and the final video is uploaded to your YouTube channel.

## Installation and Setup

### Step 1: Clone the Repository

```bash
git clone <repository_url>
cd <repository_directory>
```

### Step 2: Configure API Keys and Settings

This application requires API keys from OpenAI, Stability AI, and Google (for YouTube).

#### A. OpenAI and Stability AI Configuration

1.  **Get API Keys:**
    -   Create an account and get an API key from [OpenAI](https://platform.openai.com/api-keys).
    -   Create an account and get an API key from [Stability AI](https://platform.stability.ai/account/keys).
2.  **Edit `config.json`:**
    -   Open the `config.json` file.
    -   Paste your API keys into the `api_key` fields for `llm_generator` and `stability_ai`.
    -   Customize the `theme` and `prompt_count` for the `llm_generator` to guide the video's content.

#### B. YouTube API Credentials

1.  **Download Credentials:**
    1.  Go to the [Google Cloud Console](https://console.cloud.google.com/).
    2.  Create a new project and enable the **YouTube Data API v3**.
    3.  Create an **OAuth client ID** for a **Desktop app**.
    4.  Download the JSON file.
2.  **Place Credentials:**
    -   Rename the downloaded file to `client_secret.json`.
    -   Move this file into the `credentials/` directory.

### Step 3: Choose Your Execution Method

#### Option 1: Running with Docker (Recommended)

This method handles all dependencies for you.

**1. Build the Docker Image:**
```bash
docker build -t content-grinder .
```

**2. Run the Docker Container:**
This command runs the bot and mounts your config files into the container. This ensures the bot uses your latest settings and can save authentication tokens.

```bash
docker run --rm -it -v "$(pwd)/config.json:/app/config.json" -v "$(pwd)/credentials:/app/credentials" content-grinder
```

**First-time YouTube Authentication:**
When you run the bot for the first time, you will need to authorize it to access your YouTube account. The process is manual and works as follows:
1.  The application will print a long URL to the console. Copy this URL.
2.  Paste the URL into your web browser and log in to your Google account.
3.  Grant the application permission to upload videos on your behalf.
4.  After granting permission, your browser will redirect to a page that may show a "This site can’t be reached" error. **This is expected.** The important part is the URL in your browser's address bar.
5.  Look for the part of the URL that says `code=`. Copy the long string of characters that comes **immediately after** `code=` and before the `&scope=` part.
6.  Paste this code into the terminal when prompted for the "authorization code".

A `youtube_credentials.json` file will be created in your `credentials` directory. You will only need to do this once.

**Note on Debugging:** During this first-time authentication, you will see detailed log messages from the Google API libraries in your console. This is intentional and provides verbose information that can be helpful for debugging if you encounter any issues.

---

### Option 2: Running Locally with Python

**1. Install Dependencies:**
```bash
pip install -r requirements.txt
```

**2. Run the Bot:**
Make sure you have completed the setup in Step 2. Then, run the application:
```bash
python main.py
```