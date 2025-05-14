# Main
# Check pythonanywhere.com instance for ref

from MapFetcher import RI_MapFetcher
import requests

# Initialize
api_key = 'LhMzXgy2kWSqeCJZwc5XYClmjw9vvkIh'
fetcher = RI_MapFetcher(api_key)

# Fetch RI state map
# state_map = fetcher.get_state_map()
# state_map.show()

# Fetch map of Providence
# prov_map = fetcher.get_town_map('Providence')
# prov_map.show()

# Fetch traffic incidents (via MapQuest traffic API)
traffic_url = f'https://www.mapquestapi.com/traffic/v2/incidents?key={api_key}&boundingBox=42,-71,41,-72&filters=construction,incidents'
response = requests.get(traffic_url)
response.raise_for_status()
traffic_data = response.json()

# Print summary of incidents
for incident in traffic_data.get('incidents', []):
    print(f"{incident['shortDesc']} at ({incident['lat']}, {incident['lng']})")
