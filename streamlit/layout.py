import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import altair as alt
import pytz
from Home import get_forecast_only
import folium
from streamlit_folium import st_folium


# Generate Altair chart for the 16-day pedestrian forecast
def generate_forecast_chart(street):
    df = get_forecast_only()

    hourly_data = df[[street]].reset_index()
    hourly_data.columns = ['Timestamp', 'Pedestrian Count']
    hourly_data['Timestamp'] = hourly_data['Timestamp'] + timedelta(hours=11)
    
    # Add a column for weekday
    hourly_data['Weekday'] = hourly_data['Timestamp'].dt.strftime('%A')  # Day name

    # Filter for first occurrence of each day (or any specific rule you want)
    weekday_lines = hourly_data[hourly_data['Timestamp'].dt.hour == 0]  # Midnight for each day

    # Create the main line chart
    line_chart = alt.Chart(hourly_data).mark_line(point=True).encode(
        x=alt.X(
            'Timestamp:T',
            title='Time',
            axis=alt.Axis(
                format='%A %d-%m',  # Day of the week and date
                tickCount='day',       # Show ticks only for daily intervals
            )
        ),
        y=alt.Y('Pedestrian Count:Q', title='Pedestrian Count'),
        tooltip=[
            alt.Tooltip('Timestamp:T', title='Hour', format='%H:%M'),
            alt.Tooltip('Timestamp:T', title='Date', format='%d-%m-%y'),
            alt.Tooltip('Pedestrian Count:Q', title='Pedestrian Count')
        ]
    )

    # Add vertical lines for each weekday marker
    vertical_lines = alt.Chart(weekday_lines).mark_rule(color='gray', strokeDash=[5, 5]).encode(
        x=alt.X('Timestamp:T', title=None)  # Align with the x-axis
    )

    # Combine the line chart and vertical lines
    chart = (line_chart + vertical_lines).properties(
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

def map_one(street):
    # Create a folium map
    m = folium.Map(location=[-37.80, 144.966], zoom_start=13, tiles="CartoDB positron")

    if street == "Little Collins St-Swanston St (East)":
        folium.Marker(
            location=[-37.814442, 144.966106],
            popup="Little Collins St-Swanston St (East)",
            icon=folium.Icon(color="blue", icon="1", prefix="fa")
        ).add_to(m)

    elif street == "Lonsdale St (South)":
        folium.Marker(
            location=[-37.811053, 144.966677],
            popup="Lonsdale St (South)",
            icon=folium.Icon(color="purple", icon="2", prefix="fa")
        ).add_to(m)
    
    elif street == "Melbourne Central":
        folium.Marker(
            location=[-37.811042, 144.964422],
            popup="Melbourne Central",
            icon=folium.Icon(color="green", icon="3", prefix="fa")
        ).add_to(m)

    elif street == "Chinatown-Lt Bourke St (South)":
        folium.Marker(
            location=[-37.811601, 144.968333],
            popup="Chinatown-Lt Bourke St (South)",
            icon=folium.Icon(color="red", icon="4", prefix="fa")
        ).add_to(m)

    elif street == "Faraday St-Lygon St (West)":
        folium.Marker(
            location=[-37.798773, 144.967363],
            popup="Faraday St-Lygon St (West)",
            icon=folium.Icon(color="darkgreen", icon="5", prefix="fa")
        ).add_to(m)

    st_folium(m, width=400, height=300)

    return m



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
        col = st.columns((4, 7), gap="medium")

        with col[0]:
            subcol1, _,subcol2 = st.columns((10,1,10), gap="medium")
            with subcol1:
                st.markdown("#### Pedestrian Sensor Points")
                map_one(street)
            with subcol2:
                st.markdown("#### Comparison with last week")
                current_avg, previous_avg, delta = calculate_weekly_comparison(st.session_state["final_df"], street)
                st.metric(
                    label="Tomorrows Avg",
                    value=f"{int(current_avg)}",
                    delta=f"{delta:+.1f}",
                    help="Comparison to the previous week's daily average pedestrian count.",
                )

        # TODO Add min max values in a table
            st.write("#### MINMAX")

        with col[1]:
            st.markdown("#### 4-Day Forecast")
            forecast_chart = generate_forecast_chart(street)
            st.altair_chart(forecast_chart, use_container_width=True)


            forecast_only = get_forecast_only()
            selected_day = st.selectbox("Select a Day", np.unique(forecast_only[street].index.date))
            ### TODO Add list for hourly values

    else:
        st.error("No data available. Please run the forecast first, by entering the Home page.")
