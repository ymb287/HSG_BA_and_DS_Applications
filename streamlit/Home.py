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
import altair as alt

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
        location=[-37.798773, 144.967363],
        popup="Faraday St-Lygon St (West)",
        icon=folium.Icon(color="darkgreen", icon="2", prefix="fa")
    ).add_to(m)
    
    folium.Marker(
        location=[-37.811042, 144.964422],
        popup="Melbourne Central",
        icon=folium.Icon(color="green", icon="3", prefix="fa")
    ).add_to(m)

    folium.Marker(
        location=[-37.811601, 144.968333],
        popup="Chinatown-Lt Bourke St (South)",
        icon=folium.Icon(color="red", icon="4", prefix="fa")
    ).add_to(m)

    folium.Marker(
        location=[-37.811053, 144.966677],
        popup="Lonsdale St (South)",
        icon=folium.Icon(color="purple", icon="5", prefix="fa")
    ).add_to(m)

    st_folium(m, width=700)

    return m


def get_forecast_only():
    # Format the data
    melbourne_tz = pytz.timezone("Australia/Melbourne")
    forecast_df = st.session_state["final_df"]
    forecast_df.index = pd.to_datetime(forecast_df.index, utc=True)
    forecast_df.index = forecast_df.index.tz_convert(melbourne_tz)
    today = datetime.now(melbourne_tz).date()
    forecast_only  = forecast_df[forecast_df.index.date >= today]
    return forecast_only

def get_daily(df):
    daily_prep = df.copy()
    daily_prep['day'] = daily_prep.index.date
    valid_days = daily_prep.groupby('day').filter(lambda x: len(x) == 24)


    daily_totals = valid_days.groupby('day').sum(numeric_only=True)
    daily_totals.index.name = 'Date'

    daily_totals = daily_totals[street_list]
    daily_totals.reset_index(inplace=True)
    daylist = daily_totals['Date']
    return daily_totals, daylist

street_list = [
    'Little Collins St-Swanston St (East)', 
    'Faraday St-Lygon St (West)', 
    'Melbourne Central',
    'Chinatown-Lt Bourke St (South)',
    'Lonsdale St (South)'
]

# Main Forecst
get_forecast_once()

# Display
st.title("Pedestrian Forecast for Melbourne")

if st.session_state["final_df"] is not None:

    forecast_only = get_forecast_only()

    col = st.columns((4, 3), gap='medium')

    with col[0]:
        st.markdown('#### Pedestrian Sensor Points', help = 'Sensor points for pedestrian activity in Melbourne')
        map()


    with col[1]:
        st.markdown('#### Forecast for all streets', help = 'Forecast for cummulative pedestrian activity for a chosen day')

        daily_totals, daylist = get_daily(forecast_only)

        chosen_day = st.selectbox("Select a Day", daylist)
        chosen_day_data = daily_totals[daily_totals['Date'] == chosen_day]

        melted_data = chosen_day_data.melt(
            id_vars=['Date'], 
            var_name='Street', 
            value_name='Total Pedestrians'
        )

        # Exchange the street names with numbers and save the mapping
        street_mapping = {street: i+1 for i, street in enumerate(street_list)}
        melted_data['Street Number'] = melted_data['Street'].map(street_mapping)

        # Create Altair bar chart
        fig = alt.Chart(melted_data).mark_bar(size=50).encode(
            x=alt.X('Street Number:N', title='Street', axis=alt.Axis(labelAngle=0)),
            y=alt.Y('Total Pedestrians:Q', title='Pedestrian Count'),
            tooltip=[
                alt.Tooltip('Street:N', title='Street'),
                alt.Tooltip('Total Pedestrians:Q', title='Total Pedestrians')
            ]
        ).properties(
            title=f'Pedestrian Activity for {chosen_day}',
            width=800,
            height=400
        )

        # Display the chart in Streamlit
        st.altair_chart(fig, use_container_width=True)
        st.markdown("##### Legend")
        for key, value in street_mapping.items():
            sub_col_legend = st.columns((1,7))
            sub_col_legend[0].write(f"{value}")
            sub_col_legend[1].write(f"{key}")

