import pandas as pd
import numpy as np
import re
from datetime import datetime, timedelta
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

        # Create lagged features for multiple days
        for lag in range(1, 8):  # Lag features for 1 to 7 days
            crypto_data[f'price_lag_{lag}'] = crypto_data['price'].shift(lag)
            crypto_data[f'news_sentiment_lag_{lag}'] = crypto_data['news_sentiment'].shift(lag)
        
        crypto_data.dropna(inplace=True)
        logging.info(f"Preprocessed dataset: {file_path}")
        return crypto_data
    except Exception as e:
        logging.error(f"Failed to preprocess data: {e}")
        return pd.DataFrame()

btc_data = preprocess_crypto_data('data loader/Combined_BTC_Data.csv', sentiment_data)
eth_data = preprocess_crypto_data('data loader/Combined_ETH_Data.csv', sentiment_data)
sol_data = preprocess_crypto_data('data loader/Combined_SOL_Data.csv', sentiment_data)

# Define a function to train the model and predict prices for a given time period
def train_and_predict(data, coin_name, days_ahead):
    if data.empty:
        logging.error(f"No data available for {coin_name}")
        return None

    # Prepare training and testing data
    feature_columns = [f'price_lag_{lag}' for lag in range(1, 8)] + [f'news_sentiment_lag_{lag}' for lag in range(1, 8)] + ['volume']
    X = data[feature_columns]
    y = data['price']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train the model
    model = RandomForestRegressor(random_state=42)
    model.fit(X_train, y_train)

    # Evaluate the model
    y_pred = model.predict(X_test)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    logging.info(f"{coin_name} Model RMSE: {rmse}")

    # Prepare data for prediction
    future_input = data.iloc[-1:].copy()
    for lag in range(1, 8):
        future_input[f'price_lag_{lag}'] = future_input['price']
        future_input[f'news_sentiment_lag_{lag}'] = future_input['news_sentiment']
    
    # Predict prices for the given time period
    future_prices = []
    for day in range(1, days_ahead + 1):
        future_price = model.predict(future_input[feature_columns])[0]
        future_prices.append(future_price)
        
        # Shift the lagged features for the next prediction
        for lag in range(7, 1, -1):
            future_input[f'price_lag_{lag}'] = future_input[f'price_lag_{lag-1}']
            future_input[f'news_sentiment_lag_{lag}'] = future_input[f'news_sentiment_lag_{lag-1}']
        future_input['price_lag_1'] = future_price

    logging.info(f"Predicted Future Prices for {coin_name} for {days_ahead} days: {future_prices}")
    print(f"Predicted Future Prices for {coin_name} for {days_ahead} days: {future_prices}")
    return model, future_prices

# Predict future prices for BTC, ETH, and SOL for 30 days
btc_model, btc_future_prices = train_and_predict(btc_data, "Bitcoin", days_ahead=30)
eth_model, eth_future_prices = train_and_predict(eth_data, "Ethereum", days_ahead=30)
sol_model, sol_future_prices = train_and_predict(sol_data, "Solana", days_ahead=30)


