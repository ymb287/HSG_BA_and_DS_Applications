import pandas as pd
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import xgboost as xgb
from sklearn.metrics import mean_absolute_percentage_error
import numpy as np
import os
import xgboost as xgb
from xgboost import XGBRegressor
import joblib
import pandas as pd
import requests, json

def load_model(filename):
    """Load a model from a file."""
    if os.path.exists(filename):
        return joblib.load(filename)
    else:
        return None

def jakob_data_2():
    csv_path = os.path.join(os.path.dirname(__file__), 'final_df.csv')

    df = pd.read_csv(csv_path, parse_dates=True, index_col=0)
    df.index = pd.to_datetime(df.index)
    scaler = MinMaxScaler()
    weather_features = ['temp', 'humidity', 'rain_1h', 'clouds_all']
    df[weather_features] = scaler.fit_transform(df[weather_features])
    # Separate features and target
    target_columns = [
        'Little Collins St-Swanston St (East)', 
        'Faraday St-Lygon St (West)', 
        'Melbourne Central',
        'Chinatown-Lt Bourke St (South)',
        'Lonsdale St (South)'
    ]

    # Add lagged features (they capture pedestrian flow from the previous hour)
    for sensor in target_columns:
        df[f'{sensor}_Lag_1'] = df[sensor].shift(1)

    # Add rolling averages (capture the short term trends over the last 7 hours)
    for sensor in target_columns:
        df[f'Rolling_7_{sensor}'] = df[sensor].rolling(window=7, min_periods=1).mean()

    #Editing the feature list
    # Adding hour as a feature
    df['Hour'] = df.index.hour

    # interaction feature
    df['Rain_Holiday'] = df['rain_1h'] * df['IsPublicHoliday']

    features = [
        'IsPublicHoliday', 'Hour',
        'Weekday_2', 'Weekday_3', 'Weekday_4', 'Weekday_5', 'Weekday_6', 'Weekday_7',
        'Month_2', 'Month_3', 'Month_4', 'Month_5', 'Month_6', 'Month_7', 'Month_8', 'Month_9', 'Month_10', 'Month_11', 'Month_12',
        'Season_Spring', 'Season_Summer', 'Season_Winter',
        'temp', 'humidity', 'rain_1h', 'clouds_all'
    ] + \
    [f'Rolling_7_{sensor}' for sensor in target_columns] + \
    [f'{sensor}_Lag_1' for sensor in target_columns]

    train = df[df.index < "2024-10-16"]
    test = df[df.index >= "2024-10-16"]

    X_train = train[features]
    X_test = test[features]
    y_train = train[target_columns]
    y_test = test[target_columns]

    return X_train, X_test, y_train, y_test


def model(street):
    X_train, X_test, y_train, y_test = jakob_data_2()

    model_path = f"streamlit/models/{street}_model.joblib"

    model = load_model(model_path)

    predictions_test = model.predict(X_test)

    # Prepare the result DataFrame
    forecast_df = pd.DataFrame({
        'Timestamp': X_test.index,
        'True Count': y_test[street].values,
        'Predicted Count': predictions_test.round().astype(int)

    })

    return forecast_df