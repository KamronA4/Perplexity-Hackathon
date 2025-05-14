# app.py
# app file for streamlit deployment.

import streamlit as st
import folium
from streamlit_folium import st_folium
from streamlit_autorefresh import st_autorefresh
from MapFetcher import RI_MapFetcher
import csv
import os

# Init
file = ''
with open(file, mode='r') as f:
    reader = csv.DictReader(f)
    incidents = []
    for row in reader:
        incidents.append(row)

# Streamlit component
st_autorefresh(interval=15 * 60 * 1000)  # refresh every 15 minutes to avoid crashing

st.title("Rhode Island Traffic Map")

# Town input
town = st.text_input("Enter a Rhode Island town name:", "Providence")

# Town output
try:
    lat, lng = fetcher.get_town_coords(town)
    st.success(f"Showing map for {town} at ({lat}, {lng})")
except Exception as e:
    st.error(f"Error fetching town coordinates: {e}")
    st.stop()

# Folium map component
m = folium.Map(location=[lat, lng], zoom_start=12)

# Traffic output (use a bounding box covering all of RI)
incidents = fetcher.get_traffic_incidents()
for incident in incidents:
    folium.Marker([incident['lat'], incident['lng']], popup=incident['shortDesc'], icon=folium.Icon(color='red' if incident['severity'] > 2 else 'orange')).add_to(m)

# Display the folium map w/ features in Streamlit
st_folium(m, width=700, height=500)
