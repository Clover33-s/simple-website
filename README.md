# CryptoTracker: Advanced Cryptocurrency Analysis Tool

CryptoTracker is a full-stack web application designed to provide advanced analysis of the cryptocurrency market. It offers real-time data, interactive historical charts, and a unique AI-powered sentiment analysis feature to give users a comprehensive view of the top cryptocurrencies.

This project was built from the ground up to be a powerful, extensible platform for developing innovative crypto analysis tools.

## Features

*   **Real-Time Data**: View a dynamic table of the top 100 cryptocurrencies, including price, market cap, and 24-hour change, sourced from the CoinGecko API.
*   **Interactive Charts**: Click on any cryptocurrency to view its 30-day price history in an interactive chart, powered by Chart.js.
*   **AI-Powered Sentiment Analysis**: Get an at-a-glance view of the market mood with our sentiment analysis feature, which analyzes news headlines to provide a positive, neutral, or negative score for each coin.
*   **Dockerized Environment**: The entire application is containerized with Docker, ensuring a consistent and easy-to-manage development and deployment experience.

## Technology Stack

*   **Backend**: Python with Flask
*   **Frontend**: HTML, Tailwind CSS, JavaScript, Chart.js
*   **Data Source**: CoinGecko API
*   **Sentiment Analysis**: TextBlob
*   **Containerization**: Docker

## Prerequisites

Before you begin, ensure you have the following installed:

*   **Python 3.8+**: [Installation Guide](https://www.python.org/downloads/)
*   **pip**: Should be included with your Python installation.
*   **Docker**: [Installation Guide](https://docs.docker.com/get-docker/) (Recommended for easiest setup)

## How to Run the Application

There are two ways to run the application: using Docker (recommended) or running it directly with Python.

### Option 1: Running with Docker (Recommended)

This is the simplest way to get the application running, as it handles all dependencies and configuration automatically.

1.  **Build and Run the Docker Container**:
    Open a terminal in the project root and run the following command. Note that the first time you run this, it may take a few minutes to download the necessary images and build the container.

    ```bash
    docker-compose up --build
    ```

    You can also run it in detached mode (in the background) by adding the `-d` flag:

    ```bash
    docker-compose up --build -d
    ```

2.  **Access the Application**:
    Once the container is running, open your web browser and navigate to:
    [http://localhost:5000](http://localhost:5000)

### Option 2: Running with a Local Python Environment

If you prefer not to use Docker, you can run the application directly on your machine.

1.  **Install Dependencies**:
    Navigate to the project root in your terminal and install the required Python packages using `pip`.

    ```bash
    pip install -r requirements.txt
    ```

2.  **Run the Flask Server**:
    Once the dependencies are installed, start the Flask application.

    ```bash
    python app/app.py
    ```

3.  **Access the Application**:
    The server will now be running. Open your web browser and navigate to:
    [http://localhost:5000](http://localhost:5000)


## API Endpoints

The application exposes the following API endpoints:

*   `GET /api/coins`
    *   **Description**: Fetches a list of the top 100 cryptocurrencies by market capitalization.
    *   **Returns**: A JSON array of coin objects.

*   `GET /api/coins/<coin_id>/history`
    *   **Description**: Fetches the market chart data for the last 30 days for a specific coin.
    *   **`coin_id`**: The ID of the coin (e.g., `bitcoin`, `ethereum`).
    *   **Returns**: A JSON object containing historical price and market cap data.

*   `GET /api/coins/<coin_id>/sentiment`
    *   **Description**: Returns the AI-powered sentiment analysis for a specific coin based on simulated news headlines.
    *   **`coin_id`**: The ID of the coin (e.g., `bitcoin`, `ethereum`).
    *   **Returns**: A JSON object with the sentiment (`positive`, `neutral`, or `negative`) and the polarity score.