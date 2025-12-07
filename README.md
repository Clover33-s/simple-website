# Telephone Translator

A web application that uses the "Telephone" game concept with Google Translate. It translates your text through `N` random languages and then back to English (or the original language), often resulting in funny and unexpected changes.

## Features

*   **Randomized Path:** Selects `N` random languages from a curated list of supported languages.
*   **Deep Translator:** Uses `deep-translator` (Google Translate) for free translation.
*   **Simple UI:** Clean interface built with Tailwind CSS.
*   **Dockerized:** Easy to deploy with Docker.

## Running Locally

1.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

2.  **Run the App:**
    ```bash
    python app/app.py
    ```

3.  **Open Browser:**
    Go to `http://localhost:5000`

## Running with Docker

1.  **Build and Run:**
    ```bash
    docker-compose up --build
    ```

2.  **Open Browser:**
    Go to `http://localhost:5000`

## Configuration

*   **N (Hops):** You can adjust the number of translation hops in the UI (Default: 5, Max: 20).
