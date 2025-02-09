from flask import Flask, request, jsonify
import os
import pandas as pd
import numpy as np
from argparse import Namespace
from models.LSTM import MyLSTM  # Import your LSTM model
from train3 import load_data, prepare_data  # Import necessary functions from train3.py

app = Flask(__name__)

# Load the dataset and initialize the model
btc_data_path = os.path.join("data_loader", "Combined_BTC_Data.csv")
df = load_data(btc_data_path, include_date_for_time_series=False)

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

# Train the model on the entire dataset
data = prepare_data(df, look_back=5)
train_data = data
train_data_df = pd.DataFrame(train_data, columns=[f"feature_{i}" for i in range(train_data.shape[1] - 1)] + ['Price'])
lstm_model.fit(train_data_df)

@app.route('/predict', methods=['POST'])
def predict():
    # Get the selected coin and time period from the request
    data = request.json
    coin = data.get('coin')
    time_period = data.get('time_period')

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
