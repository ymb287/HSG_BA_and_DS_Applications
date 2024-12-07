import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import altair as alt
import pytz
from Home import get_forecast_only

# Generate Altair chart for the 16-day pedestrian forecast
def generate_forecast_chart(street):
    df = get_forecast_only()

    hourly_data = df[[street]].reset_index()
    hourly_data.columns = ['Timestamp', 'Pedestrian Count']
    
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
def calculate_weekly_comparison(df, street):
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

def render_page(street):
    # Set up Streamlit page
    st.set_page_config(
        page_title=f"Pedestrian Forecast: {street}",
        page_icon="👣",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    alt.themes.enable("dark")

    # Page Title
    st.markdown(f"### Pedestrian Forecast for {street}")

    if st.session_state["final_df"] is not None:
        # Main content
        col = st.columns((3, 7), gap="medium")
        with col[0]:
            st.markdown("#### Comparison with last week")
            current_avg, previous_avg, delta = calculate_weekly_comparison(st.session_state["final_df"], street)
            st.metric(
                label="Tomorrows Avg",
                value=f"{int(current_avg)}",
                delta=f"{delta:+.1f}",
                help="Comparison to the previous week's daily average pedestrian count.",
            )

        with col[1]:
            st.markdown("#### 4-Day Forecast")
            forecast_chart = generate_forecast_chart(street)
            st.altair_chart(forecast_chart, use_container_width=True)

    else:
        st.error("No data available. Please run the forecast first, by entering the Home page.")
