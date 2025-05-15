# app.py
# app file for streamlit deployment.

# Need: Mapfetcher.get_town_coords()

import streamlit as st
import folium
from streamlit_folium import st_folium
from streamlit_autorefresh import st_autorefresh
from MapFetcher import RI_MapFetcher
import datetime
import pandas as pd
import csv
import os

# Init

# Access 'traffic_incidents.csv'
file_path = 'code/traffic_incidents.csv'
if os.path.exists(file_path):
    try:
        incidents = pd.read_csv(file_path)

        if incidents.empty or not {'timestamp', 'lat', 'lng', 'location', 'severity', 'description'}.issubset(incidents.columns):
            st.error("The CSV file is empty or missing required columns.")
            st.stop()

        # Process .csv data
        incidents['timestamp'] = pd.to_datetime(incidents['timestamp'])
        incidents['date'] = incidents['timestamp'].dt.date
        incidents['hour'] = incidents['timestamp'].dt.hour

    except Exception as e:
        st.error(f"Error reading CSV file: {e}")
        st.stop()
else:
    st.error(f"File not found: {file_path}")
    st.stop()

# Streamlit component
st_autorefresh(interval=15 * 60 * 1000)  # Refresh every 15 minutes to avoid crashing

st.title('Rhode Island Traffic Map')

# Filters

# Date filter
date_options = sorted(incidents['date'].unique())
today = datetime.date.today()

# Default to today if exists in data, otherwise -> first available entry
default_date = today if today in date_options else date_options[0]
default_hour = datetime.datetime.now().hour

# Streamlit sidebar with default
selected_date = st.sidebar.selectbox('Select Date', date_options, index=date_options.index(default_date))

# Hour slider
selected_hour = st.sidebar.slider('Select Hour (24H):', min_value=0, max_value=23, value=datetime.datetime.now().hour)

# Date-time Filter
filtered_incidents = incidents[
    (incidents['date'] == selected_date) & (incidents['hour'] == selected_hour)
]

# Old, ignore for now
""" # Town input
town = st.text_input('Enter a Rhode Island town name:', 'Providence')

# Town output
try:
    lat, lng = fetcher.get_town_coords(town)
    st.success(f"Showing map for {town} at ({lat}, {lng})")
except Exception as e:
    st.error(f"Error fetching town coordinates: {e}")
    st.stop() """

# Default center coordinates
lat, lng = 41.8236, -71.4222  # This is Providence

# Town input
town = st.text_input('Enter a Rhode Island town name:', 'Providence')
town_incidents = filtered_incidents[filtered_incidents['location'].str.lower() == town.lower()]
if not town_incidents.empty:
    lat = town_incidents.iloc[0]['lat']
    lng = town_incidents.iloc[0]['lng']
    st.success(f"Showing map for {town} at ({lat}, {lng})")
else:
    st.warning(f"No incidents found for {town}. Centering on Providence by default.")

# Folium map
m = folium.Map(location=[lat, lng], zoom_start=12)

# Add traffic incidents to the map
# Note: popup is where we likely want to integrate Sonar
for _, incident in filtered_incidents.iterrows():
    folium.Marker(
        location=[incident['lat'], incident['lng']],
        popup=incident['description'],
        icon=folium.Icon(color='red' if incident['severity'] > 2 else 'orange')
    ).add_to(m)

# Display the folium map w/ features in Streamlit
st_folium(m, width=700, height=500)
