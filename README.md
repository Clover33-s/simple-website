# Advanced Investing Analysis Tool

This is a command-line tool for performing advanced analysis of cryptocurrencies. It fetches historical data, calculates technical indicators, and uses a machine learning model to predict future price trends.

The entire application is containerized using Docker to ensure a consistent and easy-to-use environment.

## Prerequisites

- Docker must be installed on your system. You can find installation instructions here: [https://docs.docker.com/get-docker/](https://docs.docker.com/get-docker/)

## How to Run the Tool

1.  **Build the Docker Image:**
    Open your terminal, navigate to the project directory (where the `Dockerfile` is located), and run the following command. This will build the Docker image and install all the necessary Python dependencies.
    ```bash
    docker-compose build
    ```

2.  **Run the Analysis:**
    Once the build is complete, you can run the analysis tool using the `docker-compose run` command. You can specify which cryptocurrency to analyze by changing the `--coin` argument.

    **Example: Analyze Bitcoin**
    ```bash
    docker-compose run --rm app --coin bitcoin
    ```

    **Example: Analyze Ethereum**
    ```bash
    docker-compose run --rm app --coin ethereum
    ```

    **Example: Analyze Solana**
    ```bash
    docker-compose run --rm app --coin solana
    ```

## How It Works

The script performs the following steps:
1.  **Fetches Data:** Retrieves the last 365 days of historical price data for the specified cryptocurrency from the CoinGecko API.
2.  **Calculates Indicators:** Computes several technical indicators, including:
    - Simple Moving Averages (SMA 50, SMA 200)
    - Exponential Moving Averages (EMA 12, EMA 26)
    - Relative Strength Index (RSI)
    - Moving Average Convergence Divergence (MACD)
3.  **Predicts Trend:** Trains a linear regression model on the historical data and indicators to predict the price for the next day and indicates whether the trend is UP or DOWN.

## Files in this Project

- `main.py`: The main Python script containing all the application logic.
- `requirements.txt`: A list of all the Python libraries required for the project.
- `Dockerfile`: Instructions for Docker to build the application environment.
- `docker-compose.yml`: A configuration file for easily managing the Docker container.
- `README.md`: This file, providing instructions and information about the project.