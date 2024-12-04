import folium
import streamlit as st
from streamlit_folium import st_folium
import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px
from datetime import datetime, timedelta
import numpy as np

st.set_page_config(
    page_title="Home Page: Melbourne Map",
    page_icon="🚶‍♂️",
    layout="wide",
    initial_sidebar_state="expanded")
alt.themes.enable("dark")

def map():

    # Create a folium map centered around St. Gallen, Switzerland
    m = folium.Map(location=[-37.806, 144.966], zoom_start=15, tiles="CartoDB positron")

    # Add 3 markers with custom icons
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
        location=[-37.802133, 144.966569],
        popup="Lygon St (West)",
        icon=folium.Icon(color="orange", icon="5", prefix="fa")
    ).add_to(m)

    folium.Marker(
        location=[-37.798773, 144.967363],
        popup="Faraday St-Lygon St (West)",
        icon=folium.Icon(color="darkgreen", icon="6", prefix="fa")
    ).add_to(m)

    # Display the map in Streamlit
    st_folium(m, width=700)

    return m

def make_risk(input_response, input_text, input_color):
  if input_color == 'blue':
      chart_color = ['#29b5e8', '#155F7A']
  if input_color == 'green':
      chart_color = ['#27AE60', '#12783D']
  if input_color == 'orange':
      chart_color = ['#F39C12', '#875A12']
  if input_color == 'red':
      chart_color = ['#E74C3C', '#781F16']
    
  source = pd.DataFrame({
      "Topic": ['', input_text],
      "% value": [100-input_response, input_response]
  })
  source_bg = pd.DataFrame({
      "Topic": ['', input_text],
      "% value": [100, 0]
  })
    
  plot = alt.Chart(source).mark_arc(innerRadius=45, cornerRadius=25).encode(
      theta="% value",
      color= alt.Color("Topic:N",
                      scale=alt.Scale(
                          #domain=['A', 'B'],
                          domain=[input_text, ''],
                          # range=['#29b5e8', '#155F7A']),  # 31333F
                          range=chart_color),
                      legend=None),
  ).properties(width=130, height=130)
    
  text = plot.mark_text(align='center', color="#29b5e8", font="Lato", fontSize=32, fontWeight=700, fontStyle="italic").encode(text=alt.value(f'{input_response} %'))
  plot_bg = alt.Chart(source_bg).mark_arc(innerRadius=45, cornerRadius=20).encode(
      theta="% value",
      color= alt.Color("Topic:N",
                      scale=alt.Scale(
                          # domain=['A', 'B'],
                          domain=[input_text, ''],
                          range=chart_color),  # 31333F
                      legend=None),
  ).properties(width=130, height=130)
  return plot_bg + plot + text  

def generate_synthetic_weather_data():
    start_date = datetime.now()
    days = [start_date + timedelta(days=i) for i in range(16)]

    # Generate synthetic data
    data = {
        "Date": [day.strftime('%Y-%m-%d') for day in days],
        "Temperature (°C)": np.round(np.random.uniform(10, 25, size=16), 1),  # Random temps between 10°C and 25°C
        "Cloud %": np.random.randint(0, 101, size=16),  # Random cloud cover percentage (0-100%)
        "Rain (mm)": np.round(np.random.uniform(0, 20, size=16), 1)  # Random rainfall between 0 and 20 mm
    }

    # Convert to DataFrame
    df = pd.DataFrame(data)
    return df

col = st.columns((4, 3), gap='medium')

with col[0]:
    st.markdown('#### Data Points')
    map()

with col[1]:
    st.markdown('#### Risk')
    subcol1, subcol2 = st.columns(2)
    with subcol1:
        # Generate and display the first risk plot
        risk_chart_1 = make_risk(0, 'Zero', 'green')
        st.altair_chart(risk_chart_1, use_container_width=True)
    with subcol2:
        # Generate and display the first risk plot
        risk_chart_1 = make_risk(100, 'Hundret', 'red')
        st.altair_chart(risk_chart_1, use_container_width=True)

with col[1]:
    # Create synthetic weather DataFrame
    synthetic_weather_df = generate_synthetic_weather_data()

    # Streamlit display
    st.markdown('#### 16-Day Weather Forecast for Melbourne')
    st.dataframe(synthetic_weather_df, height=400)



