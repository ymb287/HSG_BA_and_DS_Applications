import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import altair as alt

st.set_page_config(
    page_title="Pedestrian Forecast",
    page_icon="👣",
    layout="wide",
    initial_sidebar_state="expanded")
alt.themes.enable("dark")

# Generate synthetic pedestrian data with hourly resolution
def generate_hourly_pedestrian_data():
    start_date = datetime.now()
    hours = [start_date + timedelta(hours=i) for i in range(16 * 24)]  # 16 days of hourly data

    data = {
        "Timestamp": hours,
        "Pedestrian Count": np.random.randint(100, 2000, size=len(hours)),  # Random counts between 100 and 2000
    }

    df = pd.DataFrame(data)
    df['Date'] = df['Timestamp'].dt.strftime('%Y-%m-%d')
    df['Hour'] = df['Timestamp'].dt.hour
    return df

# Calculate daily max and min pedestrian counts
def calculate_daily_summary(df):
    daily_summary = df.groupby('Date')['Pedestrian Count'].agg(['max', 'min']).reset_index()
    daily_summary.rename(columns={'max': 'Max Count', 'min': 'Min Count'}, inplace=True)
    return daily_summary

# Generate Altair chart for the 16-day pedestrian forecast
def generate_forecast_chart(df):
    daily_data = df.groupby('Date')['Pedestrian Count'].mean().reset_index()
    chart = alt.Chart(daily_data).mark_line(point=True).encode(
        x=alt.X('Date:T', title='Date'),
        y=alt.Y('Pedestrian Count:Q', title='Average Pedestrian Count'),
        tooltip=['Date:T', 'Pedestrian Count:Q']
    ).properties(width=700, height=400)
    return chart

# Comparison to the previous week
def calculate_weekly_comparison(df):
    current_week = df['Pedestrian Count'].iloc[-24*7:]  # Last 7 days
    previous_week = df['Pedestrian Count'].iloc[-24*14:-24*7]  # 7-14 days ago

    current_avg = current_week.mean()
    previous_avg = previous_week.mean()

    return current_avg, previous_avg, current_avg - previous_avg

def pivot_hourly_data(data):
    pivoted_data = data.pivot(index='Date', columns='Hour', values='Pedestrian Count')
    pivoted_data.reset_index(inplace=True)
    return pivoted_data

# Layout
hourly_data = generate_hourly_pedestrian_data()
daily_summary = calculate_daily_summary(hourly_data)

# Dropdown for day selection
selected_day = st.sidebar.selectbox("Select a Day", options=daily_summary['Date'])

st.markdown("### Pedestrian Forecast for Street 1")

# Main content
col = st.columns((3, 7), gap="medium")
with col[0]:
    st.markdown("#### Weekly Comparison")
    current_avg, previous_avg, delta = calculate_weekly_comparison(hourly_data)
    st.metric(
        label="Current Week Avg",
        value=f"{int(current_avg)}",
        delta=f"{delta:+.1f}",
        help="Comparison to the previous week's average pedestrian count."
    )


    st.markdown("#### Daily Max/Min Summary")
    st.dataframe(daily_summary, height=400)

with col[1]:
    st.markdown("#### 16-Day Forecast")
    forecast_chart = generate_forecast_chart(hourly_data)
    st.altair_chart(forecast_chart, use_container_width=True)

   # Bottom section for hourly data
    st.markdown(f"### Hourly Data for {selected_day}")
    selected_day_data = hourly_data[hourly_data['Date'] == selected_day]
    pivoted_day_data = pivot_hourly_data(selected_day_data)

    # Display the pivoted data
    st.dataframe(
        pivoted_day_data.drop(columns='Date'))
