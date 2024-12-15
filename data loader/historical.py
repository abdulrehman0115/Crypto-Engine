import pandas as pd

def preprocess_historical_data(file_paths):
    """
    Load and preprocess historical data for multiple coins.

    Args:
        file_paths (dict): Dictionary with coin names as keys and file paths as values.

    Returns:
        dict: A dictionary with coin names as keys and cleaned DataFrames as values.
    """
    historical_data = {}
    for coin, file_path in file_paths.items():
        # Load the CSV file
        df = pd.read_csv(file_path)

        # Convert 'Date' to datetime
        df['Date'] = pd.to_datetime(df['Date'])

        # Remove commas and convert numeric columns
        numeric_columns = ['Price', 'Open', 'High', 'Low']
        for col in numeric_columns:
            if col in df.columns:
                df[col] = df[col].astype(str).str.replace(',', '').astype(float)

        # Handle 'Vol.' column: remove 'K' (thousand) and 'M' (million) and convert to numeric
        if 'Vol.' in df.columns:
            df['Vol.'] = df['Vol.'].astype(str).str.replace('K', 'e3', regex=False).str.replace('M', 'e6', regex=False)
            df['Vol.'] = pd.to_numeric(df['Vol.'], errors='coerce')

        # Remove '%' and convert 'Change %' to numeric
        if 'Change %' in df.columns:
            df['Change %'] = df['Change %'].astype(str).str.replace('%', '').astype(float)

        # Store the cleaned DataFrame in the dictionary
        historical_data[coin] = df

    return historical_data

# Example usage
if __name__ == "__main__":
    # Define file paths for each coin
    file_paths = {
        "BTC": "Bitcoin Historical Data.csv",
        "ETH": "Ethereum Historical Data.csv",
        "SOL": "Solana Historical Data.csv"
    }
    # Preprocess historical data
    processed_data = preprocess_historical_data(file_paths)

    # Display info and preview for each coin
    for coin, df in processed_data.items():
        print(f"{coin} Data Info:")
        # print(df.info())
        print(df.head())


