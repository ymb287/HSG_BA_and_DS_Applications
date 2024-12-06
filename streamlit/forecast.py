import pytz
from datetime import datetime, timedelta
import pandas as pd
import requests
import numpy as np
import matplotlib.pyplot as plt
import holidays
import joblib
from tqdm import tqdm
import warnings
import streamlit as st

warnings.filterwarnings("ignore", category=FutureWarning, module="xgboost")

# API
city_name = 'Melbourne'
API_KEY = '6456aee2ec2d47df861f5e544387a73c'
lat = -37.810236
lon = 144.962765
timezone = 'Australia/Melbourne'
melbourne_tz = pytz.timezone(timezone)

# Function Definitions
def fetch_weather_data(start_time, end_time):
    # Fetch historical and forecast weather data
    historical_url = f"https://history.openweathermap.org/data/2.5/history/city?lat={lat}&lon={lon}&type=hour&start={start_time}&end={end_time}&appid={API_KEY}"
    forecast_url = f"https://pro.openweathermap.org/data/2.5/forecast/hourly?lat={lat}&lon={lon}&appid={API_KEY}"

    historical_weather = requests.get(historical_url).json()
    forecast_weather = requests.get(forecast_url).json()

    return historical_weather, forecast_weather

# Define weather formating function
def formate_weather_data_new(jason):
    # Format weather data into a DataFrame.
    df = pd.DataFrame(jason['list'])

    df['temp'] = df['main'].apply(lambda x: x['temp'] - 273.15)  # Convert Kelvin to Celsius
    df['humidity'] = df['main'].apply(lambda x: x['humidity'])
    if 'rain' in df:
        df['rain'] = df['rain'].apply(lambda x: x.get('1h', 0) if isinstance(x, dict) else 0)
    else:
        df['rain'] = 0
    df['clouds'] = df['clouds'].apply(lambda x: x['all'])
    df['datetime_melbourne'] = df['dt'].apply(
        lambda x: pytz.utc.localize(datetime.utcfromtimestamp(x)).astimezone(melbourne_tz)
    )

    df.set_index('datetime_melbourne', inplace=True)
    return df[['temp', 'humidity', 'rain', 'clouds']]

# Define function to merge and fill data
def merge_and_fill_data(historical_df, forecast_df):
    # Merge historical and forecast data, filling any gaps
    last_historical_time = historical_df.index[-1]
    first_forecast_time = forecast_df.index[0]

    if first_forecast_time > last_historical_time + pd.Timedelta(hours=1):
        missing_times = pd.date_range(
            start=last_historical_time + pd.Timedelta(hours=1),
            end=first_forecast_time - pd.Timedelta(hours=1),
            freq='H',
            tz=historical_df.index.tz
        )

        missing_data = pd.DataFrame(index=missing_times, columns=historical_df.columns)
        for col in missing_data.columns:
            missing_data[col] = np.linspace(
                historical_df.iloc[-1][col],  
                forecast_df.iloc[0][col],
                len(missing_times)
            )

        combined_df = pd.concat([historical_df, missing_data, forecast_df])
    else:
        combined_df = pd.concat([historical_df, forecast_df])

    combined_df.sort_index(inplace=True)
    return combined_df

def add_features(df, holidays_list):
    # Add public holiday and time-based features
    df['IsPublicHoliday'] = [1 if date in holidays_list else 0 for date in df.index.date]
    df['Hour'] = df.index.hour
    df['Weekday'] = df.index.weekday + 1
    df['Month'] = df.index.month
    df['Season'] = df['Month'].map({
        12: 'Winter', 1: 'Winter', 2: 'Winter',
        3: 'Spring', 4: 'Spring', 5: 'Spring',
        6: 'Summer', 7: 'Summer', 8: 'Summer',
        9: 'Fall', 10: 'Fall', 11: 'Fall'
    })
    return df

def add_lagged_features(df, target_columns):
    # Add lagged and rolling features, sticking with model structure
    for sensor in target_columns:
        df[f'{sensor}_Lag_1'] = df[sensor].shift(1)

    for sensor in target_columns:
        df[f'Rolling_7_{sensor}'] = df[sensor].rolling(window=7, min_periods=1).mean()
    return df

def generate_forecast(progress_bar=None):
        ### Generate the forecast ###
    # Load saved data
    saved_data = pd.read_csv('streamlit/pedestrian_data_filtered_2.csv', index_col=0, parse_dates=True)
    last_timestamp = saved_data.index.max()

    new_start_time = int((last_timestamp + timedelta(hours=1)).astimezone(pytz.utc).timestamp())
    new_end_time = int(melbourne_tz.localize(datetime.now() + timedelta(days=1)).astimezone(pytz.utc).timestamp())

    # Fetch weather data    
    historical_weather, forecast_weather = fetch_weather_data(new_start_time, new_end_time)

    # Process and merge new data
    historical_df = formate_weather_data_new(historical_weather)
    forecast_df = formate_weather_data_new(forecast_weather)

    combined_df = merge_and_fill_data(historical_df, forecast_df)

    australia_holidays = holidays.Australia(state='VIC')
    weather_final = add_features(combined_df, australia_holidays)

    categorical_columns = ['Weekday', 'Month', 'Season']
    weather_dummies = pd.get_dummies(weather_final, columns=categorical_columns)

    # Add Nan for sensors
    target_columns = [
        'Little Collins St-Swanston St (East)', 
        'Faraday St-Lygon St (West)', 
        'Melbourne Central',
        'Chinatown-Lt Bourke St (South)',
        'Lonsdale St (South)'
    ]

    for sensor in target_columns:
        weather_dummies[sensor] = np.nan

    # Reorder columns and add lagged features
    old_columns = ['Hour', 'Little Collins St-Swanston St (East)',
        'Faraday St-Lygon St (West)', 'Melbourne Central',
        'Chinatown-Lt Bourke St (South)', 'Lonsdale St (South)',
            'IsPublicHoliday', 'temp', 'humidity', 'rain_1h',
        'clouds_all', 'Weekday_2', 'Weekday_3', 'Weekday_4', 'Weekday_5',
        'Weekday_6', 'Weekday_7', 'Month_2', 'Month_3', 'Month_4', 'Month_5',
        'Month_6', 'Month_7', 'Month_8', 'Month_9', 'Month_10', 'Month_11',
        'Month_12', 'Season_Spring', 'Season_Summer', 'Season_Winter']

    reordered_df = weather_dummies.reindex(columns=old_columns, fill_value=0)

    lagged_df = add_lagged_features(reordered_df, target_columns)


    # Scale the data and add interaction feature
    scaler = joblib.load('streamlit/models/scaler.pkl')
    weather_features = ['temp', 'humidity', 'rain_1h', 'clouds_all']

    lagged_df[weather_features] = scaler.transform(lagged_df[weather_features])

    lagged_df['Hour'] = lagged_df.index.hour
    lagged_df['Rain_Holiday'] = lagged_df['rain_1h'] * lagged_df['IsPublicHoliday']


    # Define features for modelling
    features = [
        'IsPublicHoliday', 'Hour',
        'Weekday_2', 'Weekday_3', 'Weekday_4', 'Weekday_5', 'Weekday_6', 'Weekday_7',
        'Month_2', 'Month_3', 'Month_4', 'Month_5', 'Month_6', 'Month_7', 'Month_8', 'Month_9', 'Month_10', 'Month_11', 'Month_12',
        'Season_Spring', 'Season_Summer', 'Season_Winter',
        'temp', 'humidity', 'rain_1h', 'clouds_all'
    ] + \
    [f'Rolling_7_{sensor}' for sensor in target_columns] + \
    [f'{sensor}_Lag_1' for sensor in target_columns]


    # Combine saved and new data
    final_df = pd.concat([saved_data, lagged_df])
    final_df.sort_index(inplace=True)

    rows_to_predict = final_df[target_columns].isna().any(axis=1)
    prediction_start = final_df[target_columns].isna().idxmax()[0]

    # Initialize a progress bar
    total_rows = len(final_df[rows_to_predict])
    counter = 0

    # Prediction
    for i, row in final_df[rows_to_predict].iterrows():
        counter += 1
        progress_bar.progress(counter / total_rows)
        for street in target_columns:
            # Load the model for the specific street
            model_path = f"streamlit/models/{street}_model.joblib"
            model = joblib.load(model_path)

            # Extract features for the current row
            X_current = final_df.loc[[i], features]

            # Predict the target value for the current row
            predicted_value = round(model.predict(X_current)[0])
            predicted_value = max(0, predicted_value)
            final_df.at[i, street] = predicted_value

            # Update lagged features for the next row
            next_row_index = final_df.index.get_loc(i) + 1
            if next_row_index < len(final_df):
                next_row = final_df.iloc[next_row_index]
                final_df.at[next_row.name, f'{street}_Lag_1'] = predicted_value
                rolling_feature = f'Rolling_7_{street}'
                past_values = final_df.loc[:row.name, street].tail(7)
                final_df.at[next_row.name, rolling_feature] = past_values.mean()

        # Progress bar
        if progress_bar:
            progress_bar.progress(counter / total_rows)


    # Save the past data for faster computation
    now_melbourne = datetime.now(melbourne_tz)

    cutoff_time = now_melbourne - timedelta(hours=3)
    cutoff_df = final_df[final_df.index <= cutoff_time]
    cutoff_df.to_csv('streamlit/pedestrian_data_filtered_2.csv', index=True)

    return final_df











