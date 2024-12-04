import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import altair as alt
from modelling import model
print("-"*100)
st.set_page_config(
    page_title="Pedestrian Forecast",
    page_icon="👣",
    layout="wide",
    initial_sidebar_state="expanded")
alt.themes.enable("dark")

street = 'Faraday St-Lygon St (West)'
forecast_df = model(street)
forecast_df['Date'] = pd.to_datetime(forecast_df['Timestamp']).dt.date
forecast_df['Hour'] = pd.to_datetime(forecast_df['Timestamp']).dt.hour
print("-"*100)


# Daily summary
daily_summary = forecast_df.groupby('Date')['Predicted Count'].agg(['max', 'min']).reset_index()
daily_summary.rename(columns={'max': 'Max Count', 'min': 'Min Count'}, inplace=True)

# Altair chart for daily predictions
chart = alt.Chart(forecast_df).mark_line(point=True).encode(
    x=alt.X('Timestamp:T', title='Timestamp'),
    y=alt.Y('Predicted Count:Q', title='Pedestrian Count'),
    tooltip=['Timestamp:T', 'Predicted Count:Q', 'True Count:Q']
).properties(width=700, height=400)

# Display layout
st.markdown(f"### Pedestrian Forecast for {street}")


st.altair_chart(chart, use_container_width=True)

st.markdown("#### Daily Max/Min Summary")
st.dataframe(daily_summary)

# Hourly breakdown for a selected day
selected_day = st.sidebar.selectbox("Select a Day", options=daily_summary['Date'].astype(str))
hourly_data = forecast_df[forecast_df['Date'] == selected_day]
pivoted_hourly = hourly_data.pivot(index='Hour', columns='Date', values='Predicted Count')

st.markdown(f"#### Hourly Data for {selected_day}")
st.dataframe(pivoted_hourly)