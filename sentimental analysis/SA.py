import pandas as pd
import numpy as np
import re
from datetime import datetime
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import nltk
import requests
from bs4 import BeautifulSoup
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

nltk.download('vader_lexicon')

# Function to fetch crypto-related news from multiple RSS feeds
def fetch_crypto_news():
    rss_feeds = [
        "https://www.coindesk.com/arc/outboundfeeds/rss/",  # CoinDesk
        "https://cointelegraph.com/rss",                   # CoinTelegraph
        "https://cryptoslate.com/feed/"                    # CryptoSlate
    ]
    all_news = []

    for rss_url in rss_feeds:
        try:
            response = requests.get(rss_url, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'xml')
            items = soup.find_all('item')

            for item in items:
                title = item.title.text
                pub_date = item.pubDate.text
                all_news.append({'date': pub_date, 'text': title})
            
            logging.info(f"Fetched news from {rss_url}")
        except Exception as e:
            logging.error(f"Failed to fetch news from {rss_url}: {e}")

    # Convert to DataFrame and parse dates
    news_df = pd.DataFrame(all_news)
    news_df['date'] = pd.to_datetime(news_df['date']).dt.date
    return news_df

# Fetch crypto news
news_df = fetch_crypto_news()

# Clean text data
def clean_text(text):
    text = re.sub(r"http\S+", "", text)  # Remove URLs
    text = re.sub(r"[^a-zA-Z\s]", "", text)  # Remove non-alphabetic characters
    text = text.lower()  # Convert to lowercase
    return text

# Add sentiment scores
def add_sentiment_scores(df):
    if df.empty:
        return df
    sid = SentimentIntensityAnalyzer()
    df['clean_text'] = df['text'].apply(clean_text)
    df['sentiment_score'] = df['clean_text'].apply(lambda x: sid.polarity_scores(x)['compound'])
    return df

# Apply sentiment analysis
news_df = add_sentiment_scores(news_df)

# Aggregate sentiment scores by date
news_sentiment = news_df.groupby('date')['sentiment_score'].mean()

# Combine sentiment data
sentiment_data = pd.DataFrame({'news_sentiment': news_sentiment}).fillna(0)

# Load and preprocess cryptocurrency datasets
def preprocess_crypto_data(file_path, sentiment_data):
    try:
        crypto_data = pd.read_csv(file_path)
        crypto_data['Date'] = pd.to_datetime(crypto_data['Date'], format='mixed', errors='coerce').dt.date
        crypto_data.rename(columns={'Date': 'date', 'Price': 'price', 'Vol.': 'volume'}, inplace=True)
        crypto_data['volume'] = pd.to_numeric(crypto_data['volume'], errors='coerce').fillna(0)  # Handle non-numeric values
        crypto_data = crypto_data.merge(sentiment_data, how='left', on='date')  # Merge with sentiment data
        crypto_data.fillna(0, inplace=True)
        crypto_data['price_lag_1'] = crypto_data['price'].shift(1)
        crypto_data['news_sentiment_lag_1'] = crypto_data['news_sentiment'].shift(1)
        crypto_data.dropna(inplace=True)
        logging.info(f"Preprocessed dataset: {file_path}")
        return crypto_data
    except Exception as e:
        logging.error(f"Failed to preprocess data: {e}")
        return pd.DataFrame()

btc_data = preprocess_crypto_data('data loader/Combined_BTC_Data.csv', sentiment_data)
eth_data = preprocess_crypto_data('data loader/Combined_ETH_Data.csv', sentiment_data)
sol_data = preprocess_crypto_data('data loader/Combined_SOL_Data.csv', sentiment_data)

# Function to fetch current prices using Binance API
def fetch_current_prices():
    try:
        url = "https://api.binance.com/api/v3/ticker/price"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        # Extract specific coin prices
        prices = {
            "Bitcoin": float(next(item for item in data if item["symbol"] == "BTCUSDT")["price"]),
            "Ethereum": float(next(item for item in data if item["symbol"] == "ETHUSDT")["price"]),
            "Solana": float(next(item for item in data if item["symbol"] == "SOLUSDT")["price"])
        }
        return prices
    except Exception as e:
        logging.error(f"Failed to fetch current prices: {e}")
        return None

# Function to calculate precision
def calculate_precision(actual_price, predicted_price):
    mape = np.abs((actual_price - predicted_price) / actual_price) * 100
    mae = np.abs(actual_price - predicted_price)
    logging.info(f"Precision Metrics - MAPE: {mape:.2f}%, MAE: {mae:.2f}")
    print(f"Precision Metrics - MAPE: {mape:.2f}%, MAE: {mae:.2f}")
    return mape, mae

# Define a function to train the model and predict future prices
def train_and_predict(data, coin_name):
    if data.empty:
        logging.error(f"No data available for {coin_name}")
        return None

    # Prepare training and testing data
    X = data[['price_lag_1', 'news_sentiment_lag_1', 'volume']]
    y = data['price']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train the model
    model = RandomForestRegressor(random_state=42)
    model.fit(X_train, y_train)

    # Evaluate the model
    y_pred = model.predict(X_test)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    logging.info(f"{coin_name} Model RMSE: {rmse}")

    # Prepare the most recent data for prediction
    latest_data = data.iloc[-1]
    future_input = pd.DataFrame([{
        'price_lag_1': latest_data['price'],
        'news_sentiment_lag_1': latest_data['news_sentiment_lag_1'],
        'volume': latest_data['volume']
    }])

    # Predict the future price
    future_price = model.predict(future_input)
    logging.info(f"Predicted Future Price for {coin_name}: {future_price[0]}")
    print(f"Predicted Future Price for {coin_name}: {future_price[0]}")

    return model, future_price[0]

# Train models and predict future prices for BTC, ETH, and SOL
current_prices = fetch_current_prices()
if current_prices:
    btc_model, btc_future_price = train_and_predict(btc_data, "Bitcoin")
    eth_model, eth_future_price = train_and_predict(eth_data, "Ethereum")
    sol_model, sol_future_price = train_and_predict(sol_data, "Solana")

    # Compare predicted prices with actual current prices
    print("\nComparing Predicted vs Actual Prices:")
    btc_mape, btc_mae = calculate_precision(current_prices["Bitcoin"], btc_future_price)
    eth_mape, eth_mae = calculate_precision(current_prices["Ethereum"], eth_future_price)
    sol_mape, sol_mae = calculate_precision(current_prices["Solana"], sol_future_price)

    print(f"\nActual Current Prices: {current_prices}")
    print(f"Predicted Future Prices: Bitcoin: {btc_future_price}, Ethereum: {eth_future_price}, Solana: {sol_future_price}")
else:
    logging.error("Unable to calculate precision due to missing current prices.")


