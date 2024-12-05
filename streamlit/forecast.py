import pytz
from datetime import datetime, timedelta
import pandas as pd
import requests
import numpy as np
import matplotlib.pyplot as plt
import holidays
import joblib

# API
city_name = 'Melbourne'
API_KEY = '6456aee2ec2d47df861f5e544387a73c'
lat = -37.810236
lon = 144.962765
timezone = 'Australia/Melbourne'
melbourne_tz = pytz.timezone(timezone)
australia_holidays = holidays.Australia(state='VIC')

# Function Definitions
def fetch_weather_data(start_time, end_time):
    # Fetch historical and forecast weather data
    historical_url = f"https://history.openweathermap.org/data/2.5/history/city?lat={lat}&lon={lon}&type=hour&start={start_time}&end={end_time}&appid={API_KEY}"
    forecast_url = f"https://pro.openweathermap.org/data/2.5/forecast/hourly?lat={lat}&lon={lon}&appid={API_KEY}"

    historical_weather = requests.get(historical_url).json()
    forecast_weather = requests.get(forecast_url).json()

    return historical_data, forecast_data

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
    #Add public holiday and time-based features
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




############################################

# Load saved data
saved_data = pd.read_csv('streamlit/pedestrian_data_filtered.csv', index_col=0, parse_dates=True)

# Fetch weather data
last_timestamp = saved_data.index.max() # PROBLEMMMMMMMMMMMMMMMMMMMMMMMM
new_start_time = int((last_timestamp + timedelta(hours=1)).astimezone(pytz.utc).timestamp())
new_end_time = int((datetime.now(MELBOURNE_TZ) + timedelta(days=1)).astimezone(pytz.utc).timestamp())
    
historical_weather, forecast_weather = fetch_weather_data(new_start_time, new_end_time)

# Process and merge new data
historical_df = formate_weather_data_new(historical_weather)
forecast_df = formate_weather_data_new(forecast_weather)

combined_df = merge_and_fill_data(historical_df, forecast_df)
final_df = add_features(combined_df, australia_holidays)

############################################
# Continue
############################################


# Dummy-encode all categorical columns
categorical_columns = ['Weekday', 'Month', 'Season']
df_with_all_dummies = pd.get_dummies(final_df, columns=categorical_columns)

target_columns = [
    'Little Collins St-Swanston St (East)', 
    'Faraday St-Lygon St (West)', 
    'Melbourne Central',
    'Chinatown-Lt Bourke St (South)',
    'Lonsdale St (South)'
]

# Create NA values
for sensor in target_columns:
    df_with_all_dummies[sensor] = np.nan


old_columns = ['Hour', 'Little Collins St-Swanston St (East)',
       'Faraday St-Lygon St (West)', 'Melbourne Central',
       'Chinatown-Lt Bourke St (South)', 'Lonsdale St (South)',
        'IsPublicHoliday', 'temp', 'humidity', 'rain_1h',
       'clouds_all', 'Weekday_2', 'Weekday_3', 'Weekday_4', 'Weekday_5',
       'Weekday_6', 'Weekday_7', 'Month_2', 'Month_3', 'Month_4', 'Month_5',
       'Month_6', 'Month_7', 'Month_8', 'Month_9', 'Month_10', 'Month_11',
       'Month_12', 'Season_Spring', 'Season_Summer', 'Season_Winter']

reordered_df = df_with_all_dummies.reindex(columns=old_columns, fill_value=0)

# Add lagged features (they capture pedestrian flow from the previous hour)
for sensor in target_columns:
    reordered_df[f'{sensor}_Lag_1'] = reordered_df[sensor].shift(1)

# Add rolling averages (capture the short term trends over the last 7 hours)
for sensor in target_columns:
    reordered_df[f'Rolling_7_{sensor}'] = reordered_df[sensor].rolling(window=7, min_periods=1).mean()


# Load the scaler
scaler = joblib.load('models/scaler.pkl')

weather_features = ['temp', 'humidity', 'rain_1h', 'clouds_all']

# Apply the same scaling to reordered_df
reordered_df[weather_features] = scaler.transform(reordered_df[weather_features])

reordered_df['Hour'] = reordered_df.index.hour

# interaction feature
reordered_df['Rain_Holiday'] = reordered_df['rain_1h'] * reordered_df['IsPublicHoliday']

features = [
    'IsPublicHoliday', 'Hour',
    'Weekday_2', 'Weekday_3', 'Weekday_4', 'Weekday_5', 'Weekday_6', 'Weekday_7',
    'Month_2', 'Month_3', 'Month_4', 'Month_5', 'Month_6', 'Month_7', 'Month_8', 'Month_9', 'Month_10', 'Month_11', 'Month_12',
    'Season_Spring', 'Season_Summer', 'Season_Winter',
    'temp', 'humidity', 'rain_1h', 'clouds_all'
] + \
[f'Rolling_7_{sensor}' for sensor in target_columns] + \
[f'{sensor}_Lag_1' for sensor in target_columns]


# Combine them and sort them
final_df = pd.concat([saved_data, reordered_df])
final_df.sort_index(inplace=True)

rows_to_predict = final_df[target_columns].isna().any(axis=1)
prediction_start = final_df[target_columns].isna().idxmax()[0]


import joblib
from tqdm import tqdm

# Iterate through rows needing predictions
for i, row in tqdm(final_df[rows_to_predict].iterrows(), total=len(final_df[rows_to_predict])):
    for street in target_columns:
        # Load the model for the specific street
        model_path = f"models/{street}_model.joblib"
        model = joblib.load(model_path)

        # Extract features for the current row
        X_current = final_df.loc[[i], features]

        # Predict the target value for the current row
        predicted_value = model.predict(X_current)[0]
        predicted_value = round(predicted_value)

        # Update the DataFrame with the predicted value
        final_df.at[i, street] = predicted_value

        # Update lagged features for the next row
        next_row_index = final_df.index.get_loc(i) + 1
        if next_row_index < len(final_df):
            next_row = final_df.iloc[next_row_index]
            
            # Update lagged value for the current street
            final_df.at[next_row.name, f'{street}_Lag_1'] = predicted_value

            # Update rolling features dynamically (if applicable)
            rolling_feature = f'Rolling_7_{street}'
            past_values = final_df.loc[:row.name, street].tail(7)
            final_df.at[next_row.name, rolling_feature] = past_values.mean()



import matplotlib.pyplot as plt
# Plot the pedestrian counts

# Define Melbourne timezone
melbourne_tz = pytz.timezone("Australia/Melbourne")

# Get today's date in Melbourne time
today = datetime.now(melbourne_tz)


#figsize (450, 350)

for street in target_columns:
    plt.figure(figsize=(9, 7))#(figsize=(12, 9))
    plt.plot(final_df.index, final_df[street], label='Pedestrian Count')

    # Add a vertical line at the prediction start
    plt.axvline(x=prediction_start, color='red', linestyle='--', label='Prediction Start')
    plt.axvline(x=today, color='blue', linestyle='--', label="Today's Date (Melbourne)")

    # Add labels, title, and legend
    plt.title(f'Pedestrian Counts for {street}', fontsize=16)
    plt.xlabel('Time', fontsize=12)
    plt.ylabel('Pedestrian Count', fontsize=12)
    plt.legend()
    plt.grid()

    # Show the plot
    plt.tight_layout()
    plt.show()











