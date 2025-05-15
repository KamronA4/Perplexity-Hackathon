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
# Load data from 'traffic_incidents.csv'
file_path = os.path.join('data', 'traffic_incidents.csv')
if os.path.exists(file_path):
    try:
        incidents_chunks = pd.read_csv(file_path, chunksize=100)
        incidents = pd.concat(incidents_chunks)  # Concat the chunks into a single df

        if incidents.empty or not {'timestamp', 'lat', 'lng', 'town', 'severity', 'shortDesc'}.issubset(incidents.columns):
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

st.title("Rhode Island Traffic Map")

# Filters

# Date filter
# Extract and sort the unique date options
date_options = sorted(incidents['date'].unique())
today = datetime.date.today()

# Default to today if exists in data, otherwise -> first available entry
default_date = today if today in date_options else date_options[0]
default_hour = datetime.datetime.now().hour

# Implement Streamlit sidebar with default
selected_date = st.sidebar.selectbox("Select Date", date_options, index=date_options.index(default_date))

# Implement Hour slider
selected_hour = st.sidebar.slider("Select Hour (24H):", min_value=0, max_value=23, value=default_hour)

# Date-time Filter
filtered_incidents = incidents[
    (incidents['date'] == selected_date) & (incidents['hour'] == selected_hour)
]

# Old, ignore for now
""" # Town input
town = st.text_input("Enter a Rhode Island town name:", "Providence")

# Town output
try:
    lat, lng = fetcher.get_town_coords(town)
    st.success(f"Showing map for {town} at ({lat}, {lng})")
except Exception as e:
    st.error(f"Error fetching town coordinates: {e}")
    st.stop() """


# Town input
town = st.text_input("Enter a Rhode Island town name:", "Providence")
# Town output
lat, lng = None, None  # init values
try:
    for incident in filtered_incidents:
        if incident['town'] == town:
            lat = incident['lat']
            lng = incident['lng']
            st.success(f"Showing map for {town} at ({lat}, {lng})")
            break
    else:
        st.error(f"No incidents found for {town}")
except Exception as e:
    st.error(f"Error fetching town coordinates: {e}")
    st.stop()

if lat is None or lng is None:
    st.error("Unable to load map. Latitude and Longitude are not defined.")
    st.stop()

# Folium map component
m = folium.Map(location=[lat, lng], zoom_start=12)

# Traffic output 
# Note: popup is likely where we want to integrate Sonar
for _, incident in filtered_incidents.iterrows():
    if ('lat' in incident) and ('lng' in incident) and ('severity' in incident) and ('shortDesc' in incident):
        color = 'red' if incident['severity'] > 2 else 'orange'
        folium.Marker([incident['lat'], incident['lng']], popup=incident['shortDesc'], icon=folium.Icon(color=color)).add_to(m)

# Display the folium map w/ features in Streamlit
st_folium(m, width=700, height=500)
