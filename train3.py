import os
import pandas as pd
import numpy as np
from argparse import Namespace
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# Import all models
from models.LSTM import MyLSTM
from models.GRU import MyGRU
from models.arima import MyARIMA
from models.sarimax import Sarimax
from models.orbit import Orbit
from models.random_forest import RandomForest
from models.xgboost import MyXGboost

# File path to the combined dataset
btc_data_path = os.path.join("data_loader", "Combined_BTC_Data.csv")

# Function to load and preprocess the dataset
def load_data(file_path, include_date_for_time_series=True):
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

# Function to train model and predict future prices
def train_and_predict_future_prices(model, model_name, df, look_back=5, future_intervals=[10, 180, 1440, 10080, 43200]):
    # Prepare the data for LSTM/GRU models
    data = prepare_data(df, look_back)
    
    # Use the entire dataset for training
    train_data = data

    # Convert to DataFrame before passing to the model
    train_data_df = pd.DataFrame(train_data, columns=[f"feature_{i}" for i in range(train_data.shape[1] - 1)] + ['Price'])
    
    print(f"\nTraining {model_name} model on the entire dataset...")
    model.fit(train_data_df)

    # Predict future prices
    predictions = {}
    
    for interval in future_intervals:
        print(f"Making predictions for the next {interval} minutes...")
        
        # Prepare the input for prediction: last `look_back` data
        last_window = df.iloc[-look_back:].values.flatten().tolist()

        # Make prediction for the future time period (in minutes)
        predicted_price = model.predict(np.array([last_window]))[0]
        predictions[interval] = predicted_price
    
    # Save the predictions to a CSV file
    output_file = os.path.join("models", f"{model_name}_BTC_Future_Predictions.csv")
    predictions_df = pd.DataFrame(predictions.items(), columns=["Interval (minutes)", "Predicted Price"])
    predictions_df.to_csv(output_file, index=False)
    print(f"Future predictions saved to {output_file}")


if __name__ == "__main__":
    # Load the dataset
    df_orbit_prophet = load_data(btc_data_path, include_date_for_time_series=True)  # For Orbit and Prophet
    df_other_models = load_data(btc_data_path, include_date_for_time_series=False)  # For LSTM, GRU, etc.

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

    # Initialize models
    models = {
        "LSTM": MyLSTM(model_args),
        # You can add other models here if needed, for example:
        # "GRU": MyGRU(model_args),
        # "ARIMA": MyARIMA(model_args),
        # "SARIMAX": Sarimax(model_args),
        # "Random Forest": RandomForest(model_args),
        # "XGBoost": MyXGboost(model_args),
    }

    # Train and predict future prices with each model
    for model_name, model in models.items():
        train_and_predict_future_prices(model, model_name, df_other_models)
