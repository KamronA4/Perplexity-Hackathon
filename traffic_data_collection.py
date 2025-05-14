# traffic_data_collection.py
# this will collect traffic incidents and store them into a .csv file 

import requests
import csv
from datetime import datetime
import os
from MapFetcher import RI_MapFetcher

api_key = 'LhMzXgy2kWSqeCJZwc5XYClmjw9vvkIh'
fetcher = RI_MapFetcher(api_key)
output_csv = 'traffic_incidents.csv'
bbox = '42,-71,41,-72'  # ~ RI

def fetch_traffic_incidents():
    incidents = fetcher.get_traffic_incidents()
    return incidents

def append_to_csv(incidents, filename):
    file_exists = os.path.isfile(filename) # check if the file exists
    with open(filename, mode='a', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['timestamp', 'id', 'description', 'severity', 'lat', 'lng', 'type'] # I can separate the data more finely in colab
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        if not file_exists:
            writer.writeheader()

        for incident in incidents:
            writer.writerow({
                'timestamp': datetime.utcnow().isoformat(),
                'id': incident.get('id'),
                'description': incident.get('shortDesc'),
                'severity': incident.get('severity'),
                'lat': incident.get('lat'),
                'lng': incident.get('lng'),
                'type': incident.get('type')
            })

if __name__ == '__main__':
    try:
        incidents = fetch_traffic_incidents()
        append_to_csv(incidents, output_csv)
        print(f'{len(incidents)} incidents logged at {datetime.utcnow().isoformat()}')
    except Exception as e:
        print(f'Error: {e}')
