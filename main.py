import argparse
import pandas as pd
from pycoingecko import CoinGeckoAPI
import ta
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import numpy as np

def fetch_crypto_data(coin_id, days=365, currency='usd'):
    """
    Fetches historical market data for a given cryptocurrency from CoinGecko.
    """
    cg = CoinGeckoAPI()
    try:
        chart = cg.get_coin_market_chart_by_id(id=coin_id, vs_currency=currency, days=days)

        # Convert the data to a pandas DataFrame
        df = pd.DataFrame(chart['prices'], columns=['timestamp', 'price'])
        df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
        df.set_index('timestamp', inplace=True)

        print(f"Successfully fetched data for {coin_id}.")
        return df
    except Exception as e:
        print(f"Error fetching data for {coin_id}: {e}")
        return None

def calculate_technical_indicators(df):
    """
    Calculates technical indicators for the given DataFrame.
    """
    # Simple Moving Averages
    df['SMA_50'] = ta.trend.sma_indicator(df['price'], window=50)
    df['SMA_200'] = ta.trend.sma_indicator(df['price'], window=200)

    # Exponential Moving Average
    df['EMA_12'] = ta.trend.ema_indicator(df['price'], window=12)
    df['EMA_26'] = ta.trend.ema_indicator(df['price'], window=26)

    # Relative Strength Index (RSI)
    df['RSI'] = ta.momentum.rsi(df['price'], window=14)

    # Moving Average Convergence Divergence (MACD)
    macd = ta.trend.MACD(df['price'])
    df['MACD'] = macd.macd()
    df['MACD_signal'] = macd.macd_signal()
    df['MACD_diff'] = macd.macd_diff()

    print("Technical indicators calculated.")
    return df

def train_and_predict(df):
    """
    Trains a model to predict the next day's price and makes a prediction.
    """
    # Feature engineering
    df['price_lag_1'] = df['price'].shift(1)
    df['target'] = df['price'].shift(-1)  # Predict the next day's price

    # Drop rows with NaN values created by shifting and indicators
    df.dropna(inplace=True)

    if df.empty:
        print("Not enough data to train the model after cleaning.")
        return

    features = ['price_lag_1', 'SMA_50', 'SMA_200', 'EMA_12', 'EMA_26', 'RSI', 'MACD']

    X = df[features]
    y = df['target']

    # Use the last day for prediction, and the rest for training/testing
    X_train = X[:-1]
    y_train = y[:-1]
    X_predict = X.iloc[-1].values.reshape(1, -1)

    if len(X_train) == 0:
        print("Not enough data for training.")
        return

    # Train the model
    model = LinearRegression()
    model.fit(X_train, y_train)

    # Make a prediction for the next day
    prediction = model.predict(X_predict)

    current_price = df['price'].iloc[-1]
    print(f"\n--- Price Prediction ---")
    print(f"Current Price: ${current_price:,.2f}")
    print(f"Predicted Price for Next Day: ${prediction[0]:,.2f}")

    if prediction[0] > current_price:
        print("Trend Prediction: UP")
    else:
        print("Trend Prediction: DOWN")

def main():
    """
    Main function to run the analysis tool.
    """
    parser = argparse.ArgumentParser(description="Advanced Investing Analysis Tool")
    parser.add_argument('--coin', type=str, default='bitcoin', help='The cryptocurrency ID to analyze (e.g., bitcoin, ethereum).')
    args = parser.parse_args()

    print(f"Analyzing {args.coin}...")

    # Fetch historical data (use more days for better model training)
    historical_data = fetch_crypto_data(args.coin, days=365)

    if historical_data is not None:
        # Calculate technical indicators
        data_with_indicators = calculate_technical_indicators(historical_data.copy())

        print("\nLatest Data with Technical Indicators:")
        # Display only the most recent day's indicators
        print(data_with_indicators.tail(1))

        # Train model and predict
        train_and_predict(data_with_indicators)

if __name__ == "__main__":
    main()