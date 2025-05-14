# MapFetcher.py
# This file defines RI_MapFetcher class; 
# functions to get town coordinates based on town name in RI, as well as the traffic incidents

# class RI_MapFetcher -> init using key, then fetch loc + indicent info upon call


import requests
import streamlit as st

class RI_MapFetcher:
    def __init__(self, api_key):
        self.api_key = api_key

    @st.cache_data(ttl=900) # Kept crashing due to constant reloads, cache result for 15 mins
    def get_town_coords(_self, town_name):
        # Ref -> https://developer.mapquest.com/documentation/api/geocoding/address/get.html
        geocode_url = f'https://www.mapquestapi.com/geocoding/v1/address?key={_self.api_key}&location={town_name},RI'
        response = requests.get(geocode_url)
        response.raise_for_status()
        data = response.json()
        loc = data['results'][0]['locations'][0]['latLng']
        return loc['lat'], loc['lng']

    @st.cache_data(ttl=900)  # Kept crashing due to constant reloads, cache result for 15 mins
    def get_traffic_incidents(_self, bounding_box='42,-71,41,-72'):
        traffic_url = f'https://www.mapquestapi.com/traffic/v2/incidents?key={_self.api_key}&boundingBox={bounding_box}&filters=construction,incidents'
        response = requests.get(traffic_url)
        response.raise_for_status()
        data = response.json()
        return data.get('incidents', [])
