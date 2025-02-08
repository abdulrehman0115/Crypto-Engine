from keras.models import Sequential
from keras.layers import LSTM, Dense, Dropout, Bidirectional
from keras.callbacks import ReduceLROnPlateau
from sklearn.preprocessing import StandardScaler, MinMaxScaler
import numpy as np
import pandas as pd

class MyLSTM:
    sc_in = StandardScaler()  # StandardScaler instead of MinMaxScaler for input
    sc_out = MinMaxScaler(feature_range=(0, 1))  # Keep MinMaxScaler for output (target)

    def __init__(self, args):
        self.model = Sequential()
        self.is_model_created = False
        self.hidden_dim = args.hidden_dim
        self.epochs = args.epochs

    def create_model(self, shape_):
        # Using Bidirectional LSTM and adding more units
        self.model.add(Bidirectional(LSTM(self.hidden_dim, return_sequences=True), input_shape=(1, shape_)))
        self.model.add(Dropout(0.3))  # Increased dropout
        self.model.add(LSTM(self.hidden_dim))
        self.model.add(Dropout(0.3))  # Increased dropout
        self.model.add(Dense(1))
        self.model.compile(loss='mean_squared_error', optimizer='adam')

    def clean_data(self, data_x):
        # Replace inf values with large finite values and handle missing data
        data_x = np.nan_to_num(data_x, nan=0.0, posinf=1e10, neginf=-1e10)
        data_x = pd.DataFrame(data_x)  # Convert to DataFrame to handle missing values more easily
        data_x = data_x.fillna(0)  # Fill NaN values with 0 (or other appropriate value)
        return data_x

    def fit(self, data_x):
        data_x = np.array(data_x)
        train_x = data_x[:, 1:-1]
        train_y = data_x[:, -1]

        if not self.is_model_created:
            self.create_model(train_x.shape[1])  # Create model once
            self.is_model_created = True

        train_x = self.clean_data(train_x)  # Clean data before applying scaling
        train_y = train_y.reshape(-1, 1)
        train_y = self.sc_out.fit_transform(train_y)  # Scale target values
        train_x = self.sc_in.fit_transform(train_x)  # Scale input features (StandardScaler)
        train_x = np.array(train_x, dtype=float)
        train_y = np.array(train_y, dtype=float)
        train_x = np.reshape(train_x, (train_x.shape[0], 1, train_x.shape[1]))  # Reshape for LSTM

        # Implement learning rate reduction on plateau to adjust learning rate during training
        lr_scheduler = ReduceLROnPlateau(monitor='loss', factor=0.5, patience=5, min_lr=0.0001)

        # Fit the model with callbacks (learning rate reduction)
        self.model.fit(train_x, train_y, epochs=self.epochs, verbose=1, shuffle=False, batch_size=32, callbacks=[lr_scheduler])

    def predict(self, test_x):
        test_x = np.array(test_x, dtype=float)
        test_x = self.sc_in.transform(test_x[:, 1:])  # Normalize the test data
        test_x = np.reshape(test_x, (test_x.shape[0], 1, test_x.shape[1]))  # Reshape for LSTM
        pred_y = self.model.predict(test_x)
        pred_y = pred_y.reshape(-1, 1)
        pred_y = self.sc_out.inverse_transform(pred_y)  # Inverse scaling for the target
        return pred_y
