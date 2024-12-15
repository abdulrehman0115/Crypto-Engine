import pandas as pd
from historical import preprocess_historical_data
from binance import fetch_realtime_data

def integrate_data(historical_data, real_time_data):
    """
    Integrate historical and real-time data for multiple coins and sort by timestamp.
    
    Args:
        historical_data (dict): Historical data as a dictionary of DataFrames.
        real_time_data (dict): Real-time data as a dictionary of DataFrames.
        
    Returns:
        dict: Combined data as a dictionary of DataFrames.
    """
    combined_data = {}
    for coin in historical_data.keys():
        # Ensure column names match
        real_time_data[coin].columns = historical_data[coin].columns
        
        # Combine the datasets
        combined = pd.concat([historical_data[coin], real_time_data[coin]], ignore_index=True)
        
        # Sort by timestamp (assuming the first column is the timestamp)
        combined.sort_values(by=combined.columns[0], inplace=True)
        
        # Reset the index
        combined.reset_index(drop=True, inplace=True)
        
        combined_data[coin] = combined
    
    return combined_data


# Example usage
if __name__ == "__main__":
    # Load historical data
    file_paths = {
        "BTC": "Bitcoin Historical Data.csv",
        "ETH": "Ethereum Historical Data.csv",
        "SOL": "Solana Historical Data.csv"
    }
    historical_data = preprocess_historical_data(file_paths)
    
    # Fetch real-time data
    symbols = {
        "BTC": "BTCUSDT",
        "ETH": "ETHUSDT",
        "SOL": "SOLUSDT"
    }
    real_time_data = fetch_realtime_data(symbols)
    
    # Integrate both datasets
    combined_data = integrate_data(historical_data, real_time_data)
    
    # Save combined data to CSV files
   # Save combined data to CSV files
for coin, df in combined_data.items():
    file_name = f"Combined_{coin}_Data.csv"
    
    try:
        # Load existing data
        existing_data = pd.read_csv(file_name)
        
        # Combine new and existing data
        df = pd.concat([existing_data, df], ignore_index=True)
        
    except FileNotFoundError:
        pass  # If the file doesn't exist, just use the new data

    # Ensure the timestamp column is in datetime format
    timestamp_col = df.columns[0]  # Assuming the first column is the timestamp
    df[timestamp_col] = pd.to_datetime(df[timestamp_col], errors='coerce')
    
    # Drop rows with invalid timestamps (if any)
    df.dropna(subset=[timestamp_col], inplace=True)

    # Sort the combined data by the timestamp
    df.sort_values(by=timestamp_col, inplace=True)

    # Reset the index
    df.reset_index(drop=True, inplace=True)

    # Save the final combined data
    df.to_csv(file_name, index=False)
    print(f"Saved combined data for {coin} to {file_name}")
