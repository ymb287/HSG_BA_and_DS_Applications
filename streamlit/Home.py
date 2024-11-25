import folium
import streamlit as st
from streamlit_folium import st_folium

# Sidebar for navigation
page = st.sidebar.radio("Select a Page", ["Home", "Page 1", "Page 2"])


st.title("Home Page: St. Gallen Map")


# Create a folium map centered around St. Gallen, Switzerland
m = folium.Map(location=[47.423, 9.376], zoom_start=13)

# Add 3 markers with popups
folium.Marker([47.423, 9.376], popup="Marker 1: St. Gallen").add_to(m)
folium.Marker([47.420, 9.380], popup="Marker 2: University of St. Gallen").add_to(m)
folium.Marker([47.430, 9.390], popup="Marker 3: Abbey of St. Gall").add_to(m)

# Display the map in Streamlit
st_folium(m, width=700)
