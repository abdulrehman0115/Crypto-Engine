import pandas as pd
import requests

def fetch_realtime_data(symbols):
    """
    Fetch real-time data for multiple cryptocurrency pairs from Binance API.
    
    Args:
        symbols (dict): Dictionary with coin names as keys and Binance trading pairs as values.
        
    Returns:
        dict: A dictionary with coin names as keys and DataFrames as values.
    """
    real_time_data = {}
    for coin, symbol in symbols.items():
        url = f"https://api.binance.com/api/v3/ticker/24hr?symbol={symbol}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            real_time_data[coin] = pd.DataFrame([{
                "Date": pd.Timestamp.now(),
                "Price": float(data["lastPrice"]),
                "Open": float(data["openPrice"]),
                "High": float(data["highPrice"]),
                "Low": float(data["lowPrice"]),
                "Vol.": float(data["volume"]),
                "Change %": float(data["priceChangePercent"]),
            }])
        else:
            print(f"Error fetching data for {coin}: {response.status_code}")
    
    return real_time_data

# Example usage
if __name__ == "__main__":
    symbols = {
        "BTC": "BTCUSDT",
        "ETH": "ETHUSDT",
        "SOL": "SOLUSDT"
    }
    real_time_data = fetch_realtime_data(symbols)
    for coin, df in real_time_data.items():
        print(f"{coin} real-time data preview:")
        print(df)

