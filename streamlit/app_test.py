import streamlit as st
from forecast import generate_forecast
import folium
from streamlit_folium import st_folium
import pandas as pd
import altair as alt
import plotly.express as px
from datetime import datetime, timedelta
import numpy as np
import pytz


# Setup Streamlit
st.set_page_config(
    page_title="Home Page: Melbourne Map",
    page_icon="🚶‍♂️",
    layout="wide",
    initial_sidebar_state="expanded")
alt.themes.enable("dark")

# Initialize session state
if "final_df" not in st.session_state:
    # Add a placeholder DataFrame in the session state
    st.session_state["final_df"] = None

# Functions
def get_forecast_once():
    if st.session_state["final_df"] is None:
        st.write("Generating forecast, please wait...")
        progress_bar = st.progress(0)  # Show progress bar
        st.session_state["final_df"] = generate_forecast(progress_bar=progress_bar)
        st.write("Forecast Complete!")
    else:
        pass

def map():
    # Create a folium map
    m = folium.Map(location=[-37.806, 144.966], zoom_start=15, tiles="CartoDB positron")

    folium.Marker(
        location=[-37.814442, 144.966106],
        popup="Little Collins St-Swanston St (East)",
        icon=folium.Icon(color="blue", icon="1", prefix="fa")
    ).add_to(m)

    folium.Marker(
        location=[-37.811042, 144.964422],
        popup="Melbourne Central",
        icon=folium.Icon(color="green", icon="2", prefix="fa")
    ).add_to(m)

    folium.Marker(
        location=[-37.811601, 144.968333],
        popup="Chinatown-Lt Bourke St (South)",
        icon=folium.Icon(color="red", icon="3", prefix="fa")
    ).add_to(m)

    folium.Marker(
        location=[-37.811053, 144.966677],
        popup="Lonsdale St (South)",
        icon=folium.Icon(color="purple", icon="4", prefix="fa")
    ).add_to(m)

    folium.Marker(
        location=[-37.798773, 144.967363],
        popup="Faraday St-Lygon St (West)",
        icon=folium.Icon(color="darkgreen", icon="5", prefix="fa")
    ).add_to(m)

    st_folium(m, width=700)

    return m

def get_forecast_only():
    # Format the data
    melbourne_tz = pytz.timezone("Australia/Melbourne")
    today = datetime.now(melbourne_tz).date()
    forecast_df = st.session_state["final_df"]
    forecast_df.index = pd.to_datetime(forecast_df.index, utc=True)

    forecast_only = forecast_df[forecast_df.index.date >= today]
    forecast_only.index = forecast_only.index.strftime('%Y-%m-%d %H:%M:%S')
    forecast_only.index = pd.to_datetime(forecast_only.index)
    return forecast_only

def get_daily(df):
    daily_prep = df.copy()
    daily_prep['day'] = daily_prep.index.date
    valid_days = daily_prep.groupby('day').filter(lambda x: len(x) == 24)
    daily_totals = valid_days.groupby('day').sum().sum(axis=1).reset_index()
    daily_totals.columns = ['Date', 'Total Pedestrians']
    return daily_totals


# Main Forecst
get_forecast_once()

# Display
st.title("Pedestrian Forecast")

if st.session_state["final_df"] is not None:
    # Get the forecast data
    forecast_only = get_forecast_only()

    # Get dayliy data
    daily_totals = get_daily(forecast_only)    

    col = st.columns((4, 3), gap='medium')

    with col[0]:
        st.markdown('#### Data Points')
        map()


    with col[1]:
        st.markdown('#### Forecast for Melbourne')

        # Create the bar chart
        fig = px.bar(
            daily_totals,
            x='Date',
            y='Total Pedestrians',
            title='Pedestrian Activity Forecast by Day',
            labels={'Total Pedestrians': 'Pedestrians Counted'},
            text_auto=True
        )

        # Add chart to the Streamlit app
        st.plotly_chart(fig, use_container_width=True)

else:
    st.write("No forecast data available.")
