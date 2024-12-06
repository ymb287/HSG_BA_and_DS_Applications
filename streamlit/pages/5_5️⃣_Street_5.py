import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import altair as alt
import pytz
from app_test import get_forecast_only


st.set_page_config(
    page_title="Pedestrian Forecast",
    page_icon="👣",
    layout="wide",
    initial_sidebar_state="expanded")
alt.themes.enable("dark")

street = 'Faraday St-Lygon St (West)'

# Generate Altair chart for the 16-day pedestrian forecast
def generate_forecast_chart():
    df = get_forecast_only()

    hourly_data = df[[street]].reset_index()
    hourly_data.columns = ['Timestamp', 'Pedestrian Count']
    
    print(hourly_data)

    chart = alt.Chart(hourly_data).mark_line(point=True).encode(
        x=alt.X('Timestamp:T', title='Time', axis=alt.Axis(format='%Y-%m-%d %H')),
        y=alt.Y('Pedestrian Count:Q', title='Pedestrian Count'),
        tooltip=[
            alt.Tooltip('Timestamp:T', title='Timestamp', format='%d %H:%M'),  # Full timestamp in tooltips
            alt.Tooltip('Pedestrian Count:Q', title='Pedestrian Count')
        ]
        ).properties(
        title=f'Hourly Pedestrian Counts for {street}',
        width=700,
        height=400
    )
    return chart

# Comparison to the previous week
def calculate_weekly_comparison(df):
    # Get date for tomorrow
    tomorrow = datetime.now() + timedelta(days=1)
    last_week = tomorrow - timedelta(days=7)

    # Get the rows matching those dates adn sum them
    df['Date'] = df.index.date
    tomorrow_data = df[df['Date'] == tomorrow.date()]
    last_week_data = df[df['Date'] == last_week.date()]

    current_avg = tomorrow_data[street].mean()
    previous_avg = last_week_data[street].mean()

    return current_avg, previous_avg, current_avg - previous_avg

def pivot_hourly_data(data):
    pivoted_data = data.pivot(index='Date', columns='Hour', values='Pedestrian Count')
    pivoted_data.reset_index(inplace=True)
    return pivoted_data

# Layout

st.markdown(f"### Pedestrian Forecast for {street}")

# Main content
col = st.columns((3, 7), gap="medium")
with col[0]:
    st.markdown("#### Weekly Comparison")
    current_avg, previous_avg, delta = calculate_weekly_comparison(st.session_state["final_df"])
    st.metric(
        label="Current Week Avg",
        value=f"{int(current_avg)}",
        delta=f"{delta:+.1f}",
        help="Comparison to the previous week's average pedestrian count."
    )


with col[1]:
    st.markdown("#### 16-Day Forecast")
    forecast_chart = generate_forecast_chart()
    st.altair_chart(forecast_chart, use_container_width=True)