import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import altair as alt
from modelling import model

# Setup
print("-"*100)
st.set_page_config(
    page_title="Pedestrian Forecast",
    page_icon="🚶‍♂️",
    layout="wide",
    initial_sidebar_state="expanded")
alt.themes.enable("dark")

# Prepeare calculations
street = 'Little Collins St-Swanston St (East)'
forecast_df = model(street)
forecast_df['Date'] = pd.to_datetime(forecast_df['Timestamp']).dt.date
forecast_df['Hour'] = pd.to_datetime(forecast_df['Timestamp']).dt.hour

daily_summary = forecast_df.groupby('Date')['Predicted Count'].agg(['max', 'min']).reset_index()
daily_summary.rename(columns={'max': 'Max Count', 'min': 'Min Count'}, inplace=True)

selected_day = st.sidebar.selectbox("Select a Day", options=forecast_df['Date'])






# Display layout
st.markdown(f"### Pedestrian Forecast for {street}")

col = st.columns((3, 7), gap="medium")
with col[0]:

    # THIS IS STILL A PLACEHOLDER
    st.metric(
        label="Current Week Avg",
        value=f"{int(1111)}",
        delta=f"{50:+.1f}",
        help="Comparison to the previous week's average pedestrian count."
    )

    # CHECK
    st.markdown("#### Daily Max/Min Summary")
    st.dataframe(daily_summary, height=400)

with col[1]:
    st.markdown("#### 16-Day Forecast")

    # CHECK
    chart = alt.Chart(forecast_df).mark_line(point=True).encode(
        x=alt.X('Timestamp:T', title='Timestamp'),
        y=alt.Y('Predicted Count:Q', title='Pedestrian Count'),
        tooltip=['Timestamp:T', 'Predicted Count:Q', 'True Count:Q']
    ).properties(width=900, height=400)
    chart

    st.markdown(f"#### Hourly Data for {selected_day}")
    selected_day_data = forecast_df[forecast_df['Date'] == selected_day]
    pivoted_data = selected_day_data.pivot(index='Date', columns='Hour', values='Predicted Count')
    pivoted_data.reset_index(inplace=True)
    st.dataframe(pivoted_data.drop(columns='Date').round().astype(int), width=900)
