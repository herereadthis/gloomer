import os
import json
import requests
from pprint import pprint
import sys

# from yum import utils

from utils.definitions import ROOT_DIR
from cron import logtime, logweather, logatis
# import definitions

from utils import utils


def fetch(url: str) -> list:
    res = requests.get(url)
    return json.loads(res.content)


def main():
    json_dump = os.path.join(ROOT_DIR, 'tmp', '1657290545.json')
    print(json_dump)
    print(json_dump)
    f = open(json_dump)

    # aircraft_json = fetch(url=json_dump)
    aircraft_json = json.load(f)
    aircraft = aircraft_json['aircraft']

    for plane in aircraft:
        # pprint(plane)
        hex = plane['hex']
        flight = None if 'flight' not in plane else plane['flight']
        latitude = None if 'lat' not in plane else plane['lat']
        longitude = None if 'lon' not in plane else plane['lon']
        track = None if 'track' not in plane else plane['track']
        altitude = None if 'altitude' not in plane else plane['altitude']
        speed = None if 'speed' not in plane else plane['speed']

        plane_info = {
            'hex': hex
        }
        if (flight):
            plane_info['flight'] = flight
        if (latitude):
            plane_info['latitude'] = latitude
        if (longitude):
            plane_info['longitude'] = longitude
        if (track):
            plane_info['track'] = track
        if (altitude):
            plane_info['altitude'] = altitude
        if (speed):
            plane_info['speed'] = speed
        
        pprint(plane_info)

        # print(plane['track'])
        # print(plane['lat'])
        # print(plane['lon'])
        # print(plane['altitude'])



if __name__ == '__main__':
    print('hello world')
    print(sys.argv)

    try:
        sys.argv[1]
    except IndexError:
        print("well, it WASN'T defined after all!")
        main()
    else:
        if (sys.argv[1] == 'logtime'):
            logtime.main()
        elif (sys.argv[1] == 'logweather'):
            logweather.main()
        elif (sys.argv[1] == 'logatis'):
            logatis.main()