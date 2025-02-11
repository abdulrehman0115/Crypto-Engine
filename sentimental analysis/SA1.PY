import pandas as pd
import numpy as np
import re
from datetime import datetime, timedelta
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error
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
        crypto_data['Date'] = pd.to_datetime(crypto_data['Date'], errors='coerce').dt.date
        crypto_data.rename(columns={'Date': 'date', 'Price': 'price', 'Vol.': 'volume'}, inplace=True)
        crypto_data['volume'] = pd.to_numeric(crypto_data['volume'], errors='coerce').fillna(0)  # Handle non-numeric values
        crypto_data = crypto_data.merge(sentiment_data, how='left', on='date')  # Merge with sentiment data
        crypto_data.fillna(0, inplace=True)

        # Create lagged features for 7 past days
        for lag in range(1, 8):
            crypto_data[f'price_lag_{lag}'] = crypto_data['price'].shift(lag)
            crypto_data[f'news_sentiment_lag_{lag}'] = crypto_data['news_sentiment'].shift(lag)
        
        crypto_data.dropna(inplace=True)
        logging.info(f"Preprocessed dataset: {file_path}")
        return crypto_data
    except Exception as e:
        logging.error(f"Failed to preprocess data: {e}")
        return pd.DataFrame()

btc_data = preprocess_crypto_data('Bitcoin_Data.csv', sentiment_data)
eth_data = preprocess_crypto_data('Ethereum_Data.csv', sentiment_data)
sol_data = preprocess_crypto_data('Solana_Data.csv', sentiment_data)

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

# Function to train the model and predict tomorrow's price
def train_and_predict_tomorrow(data, coin_name):
    if data.empty:
        logging.error(f"No data available for {coin_name}")
        return None

    feature_columns = [f'price_lag_{lag}' for lag in range(1, 8)] + [f'news_sentiment_lag_{lag}' for lag in range(1, 8)] + ['volume']
    X = data[feature_columns]
    y = data['price']

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = RandomForestRegressor(n_estimators=200, random_state=42)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    logging.info(f"{coin_name} Model RMSE: {rmse}")

    latest_data = data.iloc[-1].copy()

    # ✅ Ensure date is properly formatted
    try:
        if isinstance(latest_data['date'], (int, float)):  # If stored as a number, convert to string first
            latest_data['date'] = str(int(latest_data['date']))

        latest_data['date'] = pd.to_datetime(latest_data['date'], errors='coerce').date()

        if pd.isnull(latest_data['date']):  # If date conversion fails, use today's date
            logging.warning(f"{coin_name}: Date parsing issue, defaulting to today.")
            latest_data['date'] = datetime.today().date()
            
    except Exception as e:
        logging.error(f"Date processing error for {coin_name}: {e}")
        latest_data['date'] = datetime.today().date()

    future_date = latest_data['date'] + timedelta(days=1)  # ✅ Now correctly predicting tomorrow

    future_input = pd.DataFrame([latest_data[feature_columns]])
    future_price = model.predict(future_input)[0]

    logging.info(f"Predicted Price for {coin_name} on {future_date}: {future_price}")
    print(f"Predicted Price for {coin_name} on {future_date}: {future_price}")

    return model, future_price, future_date




# Train models and predict tomorrow's price for BTC, ETH, and SOL
current_prices = fetch_current_prices()
if current_prices:
    btc_model, btc_tomorrow_price, btc_date = train_and_predict_tomorrow(btc_data, "Bitcoin")
    eth_model, eth_tomorrow_price, eth_date = train_and_predict_tomorrow(eth_data, "Ethereum")
    sol_model, sol_tomorrow_price, sol_date = train_and_predict_tomorrow(sol_data, "Solana")

    print("\nComparing Predicted vs Actual Prices:")
    calculate_precision(current_prices["Bitcoin"], btc_tomorrow_price)
    calculate_precision(current_prices["Ethereum"], eth_tomorrow_price)
    calculate_precision(current_prices["Solana"], sol_tomorrow_price)

    print(f"\nActual Current Prices: {current_prices}")
    print(f"Predicted Prices for Tomorrow ({btc_date}): Bitcoin: {btc_tomorrow_price}, Ethereum: {eth_tomorrow_price}, Solana: {sol_tomorrow_price}")
else:
    logging.error("Unable to calculate precision due to missing current prices.")