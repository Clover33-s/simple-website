from flask import Flask, render_template, jsonify
from pycoingecko import CoinGeckoAPI

app = Flask(__name__)
cg = CoinGeckoAPI()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/coins')
def get_coins():
    # Fetch top 100 coins by market cap
    coins = cg.get_coins_markets(vs_currency='usd')
    return jsonify(coins)

from textblob import TextBlob

# Dummy news headlines for sentiment analysis
DUMMY_NEWS = {
    "bitcoin": [
        "Bitcoin hits new all-time high, investors are bullish!",
        "Major corporation announces massive Bitcoin investment.",
        "Bitcoin price drops amid regulatory concerns.",
        "Analyst predicts a bright future for Bitcoin.",
        "Is the Bitcoin bubble about to burst? Experts weigh in."
    ],
    "ethereum": [
        "Ethereum 2.0 upgrade promises huge scalability improvements.",
        "DeFi projects on Ethereum are booming.",
        "High gas fees on Ethereum are a major issue for users.",
        "Ethereum's potential is 'underestimated,' says tech mogul.",
        "Vitalik Buterin outlines exciting new roadmap for Ethereum."
    ],
    "dogecoin": [
        "Dogecoin price soars after tweet from Elon Musk.",
        "Experts warn that Dogecoin is a highly speculative asset.",
        "Dogecoin community rallies for a good cause.",
        "What is Dogecoin? A look at the meme coin's surprising rise.",
        "Dogecoin's value plummets as hype fades."
    ]
}

@app.route('/api/coins/<coin_id>/history')
def get_coin_history(coin_id):
    # Fetch historical data for the last 30 days
    history = cg.get_coin_market_chart_by_id(id=coin_id, vs_currency='usd', days=30)
    return jsonify(history)

@app.route('/api/coins/<coin_id>/sentiment')
def get_coin_sentiment(coin_id):
    headlines = DUMMY_NEWS.get(coin_id.lower(), [])
    if not headlines:
        return jsonify({"sentiment": "neutral", "polarity": 0})

    total_polarity = 0
    for headline in headlines:
        blob = TextBlob(headline)
        total_polarity += blob.sentiment.polarity

    avg_polarity = total_polarity / len(headlines)

    if avg_polarity > 0.1:
        sentiment = "positive"
    elif avg_polarity < -0.1:
        sentiment = "negative"
    else:
        sentiment = "neutral"

    return jsonify({"sentiment": sentiment, "polarity": avg_polarity})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)