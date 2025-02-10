from flask import Flask, request, jsonify
import os
import pandas as pd
import numpy as np
from argparse import Namespace
from models.LSTM import MyLSTM  # Import your LSTM model

app = Flask(__name__)

# Function to load and preprocess the dataset
def load_data(coin, include_date_for_time_series=True):
    # Define the file path based on the selected coin
    file_path = os.path.join("data_loader", f"combined_{coin}_Data.csv")
    
    # Load the dataset
    df = pd.read_csv(file_path)
    
    # Ensure the 'Date' column is in datetime format
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    
    # Drop rows with invalid dates
    df.dropna(subset=['Date'], inplace=True)
    
    # Sort data by date (ascending order)
    df = df.sort_values(by='Date')

    # Only drop 'Date' column for models that do not require it
    if not include_date_for_time_series:
        df.drop(columns=['Date'], inplace=True)

    # Ensure numeric columns are correctly typed
    numeric_columns = ['Price', 'Open', 'High', 'Low', 'Vol.', 'Change %']
    for col in numeric_columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')

    # Drop rows with missing values
    df.dropna(subset=numeric_columns, inplace=True)
    
    return df

# Function to prepare the data for LSTM/GRU
def prepare_data(df, look_back=5):
    data = []
    for i in range(len(df) - look_back):
        window = df.iloc[i:i + look_back].values.flatten().tolist()
        target = df.iloc[i + look_back, 0]  # Assuming 'Price' is the first column
        data.append(window + [target])
    return np.array(data)

# Define model parameters
model_args = Namespace(
    hidden_dim=64, epochs=50, 
    order=(1, 1, 1),  
    seasonal_order=(1, 1, 1, 12),
    enforce_invertibility=True, enforce_stationarity=True, 
    response_col="Price", date_col="Date",
    n_estimators=100, random_state=42,  # Used for RandomForest & XGBoost
    is_daily=True, is_hourly=False, confidence_level=0.95,  # Needed for NeuralProphet
    estimator="stan-map",  # Fix for Orbit model
    seasonality=12,
    seed=42,
    global_trend_option="linear",
    n_bootstrap_draws=100
)

# Initialize the LSTM model
lstm_model = MyLSTM(model_args)

@app.route('/predict', methods=['POST'])
def predict():
    # Get the selected coin and time period from the request
    data = request.json
    coin = data.get('coin')
    time_period = data.get('time_period')

    # Load the dataset for the selected coin
    df = load_data(coin, include_date_for_time_series=False)

    # Prepare the data for LSTM/GRU models
    data = prepare_data(df, look_back=5)
    
    # Use the entire dataset for training
    train_data = data

    # Convert to DataFrame before passing to the model
    train_data_df = pd.DataFrame(train_data, columns=[f"feature_{i}" for i in range(train_data.shape[1] - 1)] + ['Price'])
    
    # Train the model on the selected coin's dataset
    lstm_model.fit(train_data_df)

    # Prepare the input for prediction: last `look_back` data
    look_back = 5
    last_window = df.iloc[-look_back:].values.flatten().tolist()

    # Make prediction for the future time period (in minutes)
    predicted_price = lstm_model.predict(np.array([last_window]))[0][0]

    # Convert float32 to float for JSON serialization
    predicted_price = float(predicted_price)

    # Return the prediction as a JSON response
    return jsonify({
        'coin': coin,
        'time_period': time_period,
        'predicted_price': predicted_price
    })

if __name__ == '__main__':
    app.run(debug=True)