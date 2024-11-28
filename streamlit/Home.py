import folium
import streamlit as st
from streamlit_folium import st_folium


st.title("Home Page: St. Gallen Map")

# Create a folium map centered around St. Gallen, Switzerland
m = folium.Map(location=[-37.808, 144.966], zoom_start=15, tiles="CartoDB positron")

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

# Display the map in Streamlit
st_folium(m, width=700)
