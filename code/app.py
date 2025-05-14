# app.py
# app file for streamlit deployment.

# Need: Mapfetcher.get_town_coords()

import streamlit as st
import folium
from streamlit_folium import st_folium
from streamlit_autorefresh import st_autorefresh
from MapFetcher import RI_MapFetcher
import csv
import os

# Init
# Access 'traffic_incidents.csv'
file_path = os.path.join(data_folder, 'traffic_incidents.csv')
if os.path.exists(file_path):
    with open(file_path, 'r') as file:
        incidents_file = file.read()

# Create incidents dict
incidents = ''
with open(incidents_file, mode='r') as f:
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
for incident in incidents:
    folium.Marker([incident['lat'], incident['lng']], popup=incident['shortDesc'], icon=folium.Icon(color='red' if incident['severity'] > 2 else 'orange')).add_to(m)

# Display the folium map w/ features in Streamlit
st_folium(m, width=700, height=500)
