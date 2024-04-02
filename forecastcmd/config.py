import json
import os 

# Get the directory of the current file.
file_dir = os.path.dirname(__file__) 

# Construct a platform-independent path to the JSON file.
json_file_path = os.path.join(file_dir, 'data', 'zip_codes_forecast_urls.json')

# Load the JSON data, which pairs a forecast URL with each zip code.
with open(json_file_path, 'r') as json_file:
    zip_codes_dict = json.load(json_file)