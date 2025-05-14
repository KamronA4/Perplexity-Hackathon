# access 'data' from 'code':

import os
import csv

script_dir = os.path.dirname(os.path.abspath(__file__))

data_folder = os.path.join(script_dir, "..", "data")

# lists the files in 'data'
if os.path.exists(data_folder):
    for filename in os.listdir(data_folder):
        print(filename)
else:
    print(f"Error: Data folder not found at {data_folder}")

# access 'traffic_incidents.csv'
file_path = os.path.join(data_folder, "my_data.txt")
if os.path.exists(file_path):
    with open(file_path, "r") as file:
        data = file.read()
        print(data)
else:
    print(f"Error: File not found at {file_path}")
