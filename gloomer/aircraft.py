#!/usr/bin/env python

"""
write pep-8 and pylint-valid script that takes the json from a url, and outputs 
a human-readable summary of that json. Use cron to call the script every 5th 
second in a day
*/5 * * * * * /path/to/python /path/to/script.py
"""

import json
import requests

URL = "http://adsb.local:8080/data/aircraft.json"

try:
    response = requests.get(URL)
    data = json.loads(response.content)
    aircraft = data['aircraft']
    aircraft_with_flight_data = [d for d in aircraft if "lat" in d and "lon" in d]
    print(aircraft_with_flight_data)
    summary = f"JSON data summary:\nNumber of records: {len(aircraft_with_flight_data)}\n"\
            f"First record: {aircraft_with_flight_data[0]}\n"\
            f"Last record: {aircraft_with_flight_data[-1]}"
    print(summary)
except Exception as e:
    print(f"An error occurred: {e}")