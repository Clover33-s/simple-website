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

1.  **Configure the OAuth Consent Screen (Crucial Step):**
    -   Go to the [Google Cloud Console](https://console.cloud.google.com/) and select your project.
    -   From the navigation menu, go to **APIs & Services -> OAuth consent screen**.
    -   For **User Type**, select **External** and click **CREATE**.
    -   On the next page, fill out the required fields:
        -   **App name:** Give your app a name (e.g., "AI Content Bot").
        -   **User support email:** Select your email address.
        -   **Developer contact information:** Enter your email address again at the bottom of the page.
    -   Click **SAVE AND CONTINUE** through the "Scopes" and "Optional info" sections. You don't need to add anything here.
    -   Back on the dashboard, under **Publishing status**, ensure it says "Testing".

2.  **Add Your Account as a Test User:**
    -   While still on the **OAuth consent screen**, under the **"Test users"** section, click **+ ADD USERS**.
    -   Enter the Google email address you will use to log in and upload videos.
    -   Click **SAVE**. You must do this to authorize your own account to use the app.

3.  **Create and Download Credentials:**
    -   Now, go to the **Credentials** tab from the side menu.
    -   Click **+ CREATE CREDENTIALS** and select **OAuth client ID**.
    -   Choose **Desktop app** for the application type and give it a name.
    -   Click **CREATE**. From the list of OAuth 2.0 Client IDs, find your newly created credential and click the **Download JSON** icon.

4.  **Place Credentials File:**
    -   Rename the downloaded credentials JSON file to `client_secret.json`.
    -   Move this file into the `credentials/` directory.

### Step 3: Choose Your Execution Method

#### Option 1: Running with Docker (Recommended)

This method handles all dependencies for you.

**1. Build the Docker Image:**
```bash
docker build -t content-grinder .
```

**2. Run the Docker Container:**
This command runs the bot, forwards the necessary port for authentication, and mounts your config files. This ensures the bot uses your latest settings and can save authentication tokens.

```bash
docker run --rm -it -p 8080:8080 -v "$(pwd)/config.json:/app/config.json" -v "$(pwd)/credentials:/app/credentials" content-grinder
```

**First-time YouTube Authentication:**
When you run the container for the first time, you will need to authorize it to access your YouTube account:
1.  The application will print a long URL to the console. Copy this URL and paste it into your web browser.
2.  Log in to your Google account and grant the application permission.
3.  Once authorized, you will be redirected to a page confirming that the authentication flow has completed. You can then close the browser tab. The application will continue running automatically.

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