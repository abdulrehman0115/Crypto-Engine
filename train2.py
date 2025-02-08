import os
import pandas as pd
import numpy as np
from argparse import Namespace
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

from models.orbit import Orbit

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

def predict_future(model, train_data, look_back=5, time_intervals=[10, 180, 1440, 10080, 43200]):
    # Prepare the last 'look_back' data for prediction (use the most recent data point)
    last_data_point = train_data[-look_back:, :-1]  # Last 'look_back' rows excluding the target (Price)
    predictions = {}

    # Convert the last_data_point into a DataFrame to match the input format the model expects
    columns = [f"feature_{i}" for i in range(last_data_point.shape[1])]  # Create feature column names
    last_data_point_df = pd.DataFrame(last_data_point, columns=columns)
    
    # Ensure the correct columns are present and in the same order as during training
    missing_columns = set(model.sc_in.feature_names_in_) - set(last_data_point_df.columns)
    for missing_col in missing_columns:
        last_data_point_df[missing_col] = 0  # Add missing columns with 0 values
    
    # Reorder columns to match the training data feature order
    last_data_point_df = last_data_point_df[model.sc_in.feature_names_in_]

    # Now, we iterate over the time intervals and predict the future prices
    for interval in time_intervals:
        future_data_point = last_data_point_df.copy()  # Start from the most recent data point
        
        for _ in range(interval):  # Predict for the next 'interval' time steps
            # Ensure we're using the same feature order and applying the scaler consistently
            future_data_point_scaled = model.sc_in.transform(future_data_point.values)  # Apply the scaler
            future_prediction = model.predict(future_data_point_scaled)  # Predict next step
            
            # Convert predicted values back into a DataFrame for future predictions
            future_data_point_df = pd.DataFrame(future_prediction, columns=["Prediction"])
            
            # Update the data for the next prediction step
            future_data_point = future_data_point_df
        
        # Store the predicted price for the current interval
        predictions[interval] = future_data_point_df["Prediction"].iloc[-1]

    return predictions


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

    # Convert to DataFrame before passing to Orbit
    train_data_df = pd.DataFrame(train_data, columns=[f"feature_{i}" for i in range(train_data.shape[1] - 1)] + ['Price'])
    test_data_df = pd.DataFrame(test_data, columns=[f"feature_{i}" for i in range(test_data.shape[1] - 1)] + ['Price'])

    # Define model parameters
    model_args = Namespace(
        response_col="Price", 
        date_col="Date",
        estimator="stan-map",  
        seasonality=12,
        seed=42,
        global_trend_option="linear",
        n_bootstrap_draws=100
    )

    # Initialize models
    models = {
        "Orbit": Orbit(model_args),
    }

    # Train and evaluate each model
    for model_name, model in models.items():
        train_and_evaluate(model, model_name, train_data_df, test_data_df)

        # Predict future BTC prices for 10 minutes, 3 hours, 1 day, 1 week, and 1 month
        future_predictions = predict_future(model, train_data)
        print(f"Future Predictions for {model_name}: {future_predictions}")

        # Save the predictions for future prices
        output_file = os.path.join("models", f"{model_name}_BTC_Future_Predictions.csv")
        predictions_df = pd.DataFrame(future_predictions, index=["Next 10 mins", "Next 3 hours", "Next 1 day", "Next 1 week", "Next 1 month"], columns=["Predicted Price"])
        predictions_df.to_csv(output_file)
        print(f"Future predictions saved to {output_file}")
