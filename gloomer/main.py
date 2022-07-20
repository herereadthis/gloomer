import os
import json
import requests
from pprint import pprint
import sys
import toml
from geographiclib.geodesic import Geodesic
import math
geod = Geodesic.WGS84

# from yum import utils

from utils import utils
from utils.definitions import ROOT_DIR
from cron import logtime, logweather, logatis
# import definitions

from utils import utils


def fetch(url: str) -> list:
    res = requests.get(url)
    return json.loads(res.content)


    
def filter_function(plane):
    return False if 'lat' not in plane else True

def map_function(plane):
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

    print(plane_info)
    
    return plane_info


def main():
    json_dump = os.path.join(ROOT_DIR, 'tmp', '1657290554.json')
    print(json_dump)
    print(json_dump)
    f = open(json_dump)

    # aircraft_json = fetch(url=json_dump)
    aircraft_json = json.load(f)
    aircraft = aircraft_json['aircraft']

    aircraft_with_data = list(filter(filter_function, aircraft))
    # pprint(aircraft_with_data)
    formatted_aircraft = list(map(map_function, aircraft_with_data))


    # pprint(formatted_aircraft)


    config = toml.load(utils.get_config_file_path())
    adsb_config = config['adsb']
    base_latitude = adsb_config['latitude']
    base_longitude = adsb_config['longitude']
    radius = adsb_config['radius']

    for plane in formatted_aircraft:
        print('\n')
        print(plane['latitude'])
        print(plane['longitude'])

        g = geod.Inverse(base_latitude, base_longitude, plane['latitude'], plane['longitude'])

        print("The distance is {:.3f} m.".format(g['s12']))




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