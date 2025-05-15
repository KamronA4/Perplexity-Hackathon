# MapFetcher.py
# This file defines RI_MapFetcher class; 
# functions to get town coordinates based on town name in RI, as well as the traffic incidents

# class RI_MapFetcher -> init using key, then fetch loc + indicent info upon call
import requests
import streamlit as st

class RI_MapFetcher:
    def __init__(self, api_key):
        self.api_key = '9-BLy5MsFJzs8VUThVXqDeE_tx5zCHjwA9hdQxFvLj4'

    @st.cache_data(ttl=900) # cache result for 15 mins
    def get_town_coords(_self, town_name):
        # Ref: -> (geocode api) https://www.here.com/docs/bundle/geocoding-and-search-api-v7-api-reference/page/index.html
        geocode_url = f'https://geocode.search.hereapi.com/v1/geocode?q={town_name}&apiKey={_self.api_key}'
        response = requests.get(geocode_url)
        response.raise_for_status()
        data = response.json()
        loc = data['items'][0]['position']
        return loc['lat'], loc['lng']

    # Ref: -> (traffic api) https://www.here.com/docs/bundle/traffic-api-developer-guide-v7/page/topics/concepts/incidents.html
    @st.cache_data(ttl=900)  # Kept crashing due to constant reloads, cache result for 15 mins
    def get_traffic_incidents(_self, bounding_box='42,-71,41,-72'):
        traffic_url = f'https://geocode.search.hereapi.com/traffoc/6.3/incidents.json?bbox={bounding_box}&apiKey={_self.api_key}&criticality=major,minor'
        response = requests.get(traffic_url)
        response.raise_for_status()
        data = response.json()
        return data.get('TRAFFIC_ITEMS', 'TRAFFIC_ITEM')
