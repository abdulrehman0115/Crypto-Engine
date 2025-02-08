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

# Training and evaluating models
def train_and_evaluate(model, model_name, train_data, test_data):
    print(f"\nTraining {model_name} model...")
    model.fit(train_data)

    print(f"Making predictions with {model_name}...")
    
    # If test_data is a DataFrame, use column indexing for pandas
    test_features = test_data.iloc[:, :-1]  # Use pandas iloc for slicing
    
    # Convert to numpy array if needed (for prediction)
    predictions = model.predict(test_features.values)

    actual_values = test_data.iloc[:, -1].values  # Get the target values (last column)

    # Fix: Convert to NumPy array before flattening
    if isinstance(predictions, pd.Series):
        predicted_values = predictions.to_numpy().flatten()
    else:
        predicted_values = predictions.flatten()

    # Evaluate the model
    mae = mean_absolute_error(actual_values, predicted_values)
    mse = mean_squared_error(actual_values, predicted_values)
    rmse = np.sqrt(mse)
    r2 = r2_score(actual_values, predicted_values)

    print(f"\n{model_name} Model Evaluation:")
    print(f"Mean Absolute Error (MAE): {mae:.4f}")
    print(f"Mean Squared Error (MSE): {mse:.4f}")
    print(f"Root Mean Squared Error (RMSE): {rmse:.4f}")
    print(f"R-squared (R²): {r2:.4f}")

    # Save the predictions and results
    output_file = os.path.join("models", f"{model_name}_BTC_Predictions.csv")
    results_df = pd.DataFrame({
        "Actual Price": actual_values,
        "Predicted Price": predicted_values
    })
    results_df.to_csv(output_file, index=False)
    print(f"Predictions and evaluation metrics saved to {output_file}")


if __name__ == "__main__":
    # Load the dataset
    df_orbit_prophet = load_data(btc_data_path, include_date_for_time_series=True)  # For Orbit and Prophet
    df_other_models = load_data(btc_data_path, include_date_for_time_series=False)  # For LSTM, GRU, etc.

    # Prepare the data for LSTM/GRU models (using df_other_models)
    look_back = 5
    data = prepare_data(df_other_models, look_back)
    split_index = int(len(data) * 0.8)  # 80-20 train-test split
    train_data = data[:split_index]
    test_data = data[split_index:]

    # Prepare the data for Orbit/Prophet models (using df_orbit_prophet)
    # Now pass df_orbit_prophet to Orbit and Prophet models

    # Convert to DataFrame before passing to XGBoost
    train_data_df = pd.DataFrame(train_data, columns=[f"feature_{i}" for i in range(train_data.shape[1] - 1)] + ['Price'])
    test_data_df = pd.DataFrame(test_data, columns=[f"feature_{i}" for i in range(test_data.shape[1] - 1)] + ['Price'])

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
        "ARIMA": MyARIMA(model_args),
        "Orbit": Orbit(model_args),
}


    # Train and evaluate each model
    for model_name, model in models.items():
        train_and_evaluate(model, model_name, train_data_df, test_data_df)
