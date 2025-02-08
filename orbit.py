import pandas as pd
from orbit.models import DLT
import numpy as np
from sklearn.preprocessing import MaxAbsScaler


class Orbit:
    model = None
    sc_in = MaxAbsScaler()
    sc_out = MaxAbsScaler()

    def __init__(self, args):
        self.response_col = args.response_col
        self.date_col = args.date_col  # This should be the name of the date column in your data
        self.estimator = args.estimator
        self.seasonality = args.seasonality
        self.seed = args.seed
        self.global_trend_option = args.global_trend_option
        self.n_bootstrap_draws = args.n_bootstrap_draws

    def fit(self, data_x):
        # Convert NumPy array to DataFrame
        num_features = data_x.shape[1] - 1  # Exclude target column
        columns = [f"feature_{i}" for i in range(num_features)] + [self.response_col]
        data_x = pd.DataFrame(data_x, columns=columns)

        print(f"Training Data Shape: {data_x.shape}")  # Debugging step

        # Add date column (if not present) and set the correct column name
        data_x[self.date_col] = pd.date_range(start="2020-01-01", periods=len(data_x), freq="D")  # Assuming daily frequency
        data_x[self.date_col] = pd.to_datetime(data_x[self.date_col])  # Ensure datetime format

        regressors = []
        for col in data_x.columns:
            if col != self.response_col and col != self.date_col:
                regressors.append(col)

        # Ensure all values are numeric
        data_x[regressors] = data_x[regressors].astype(float)
        data_x[self.response_col] = data_x[self.response_col].astype(float)

        # Apply scaling
        data_x.loc[:, regressors] = self.sc_in.fit_transform(data_x.loc[:, regressors])
        data_x.loc[:, self.response_col] = self.sc_out.fit_transform(
            data_x.loc[:, self.response_col].values.reshape(-1, 1)
        )

        # Initialize and fit the Orbit model without point_method argument
        self.model = DLT(
            response_col=self.response_col,
            date_col=self.date_col,
            regressor_col=regressors,
            estimator=self.estimator,
            seasonality=self.seasonality,
            seed=self.seed,
            global_trend_option=self.global_trend_option,
            n_bootstrap_draws=self.n_bootstrap_draws,
        )

        # Remove point_method="mean" from the fit method
        self.model.fit(data_x)

    def predict(self, test_x):
        # Convert NumPy array to DataFrame
        num_features = test_x.shape[1] - 1  # Exclude target column
        columns = [f"feature_{i}" for i in range(num_features)] + [self.response_col]
        test_x = pd.DataFrame(test_x, columns=columns)

        # Add the same date column to test data (ensure the model receives it)
        test_x[self.date_col] = pd.date_range(start="2021-01-01", periods=len(test_x), freq="D")  # Fake dates for prediction
        test_x[self.date_col] = pd.to_datetime(test_x[self.date_col])  # Ensure datetime format

        # Ensure that test data has the same columns as training data
        missing_columns = set(self.sc_in.feature_names_in_) - set(test_x.columns)
        for missing_col in missing_columns:
            test_x[missing_col] = 0  # Add missing columns with 0 values

        # Handle regressors and apply transformations
        regressors = [col for col in test_x.columns if col != self.response_col and col != self.date_col]
        test_x[regressors] = test_x[regressors].astype(float)

        test_x.loc[:, regressors] = self.sc_in.transform(test_x.loc[:, regressors])

        predicted_df = self.model.predict(df=test_x)

        # Inverse transform predictions
        predicted_df.loc[:, "prediction"] = self.sc_out.inverse_transform(
            predicted_df.loc[:, "prediction"].values.reshape(-1, 1)
        )
        return np.array(predicted_df["prediction"])
