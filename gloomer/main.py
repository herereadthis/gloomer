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


def map_function(config):
    base_latitude = config['latitude']
    base_longitude = config['longitude']
    radius = config['radius']

    def mapper(plane):
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

        if ('latitude' in plane_info and 'longitude' in plane_info):
            geo = geod.Inverse(base_latitude, base_longitude, plane_info['latitude'], plane_info['longitude'])

            distance_meters = geo['s12']

            if (distance_meters < radius):
                plane_info['geo']  = geo
                plane_info['distance_meters'] = distance_meters
        
        return plane_info
    return mapper


def leftFn(foo):
    def rightFn(bar):
        print(f'{foo}, {bar}') 
    return rightFn

# leftFn('foo')('bar')

def filter_format_aircraft(aircraft, adsb_config):
    aircraft_with_data = list(filter(lambda plane: False if 'lat' not in plane else True, aircraft))
    formatted_aircraft = list(map(map_function(adsb_config), aircraft_with_data))
    return list(filter(lambda plane: True if 'geo' in plane else False, formatted_aircraft))


def main():
    print('Running aircraft locater.')
    config = toml.load(utils.get_config_file_path())
    adsb_config = config['adsb']

    json_dump = os.path.join(ROOT_DIR, 'tmp', '1657292399.json')
    f = open(json_dump)

    aircraft_json = json.load(f)
    aircraft = aircraft_json['aircraft']
    selected_aircraft = filter_format_aircraft(aircraft, adsb_config)

    print(f'{len(selected_aircraft)} nearby aircraft found.')

    for plane in filter_format_aircraft(aircraft, adsb_config):
        distance_meters = plane['geo']['s12']

        print('\n')
        pprint(plane)
        print("The distance is {:.3f} m.".format(distance_meters))


if __name__ == '__main__':
    def runMain():
        return main()
    
    def runScripts(argv):
        if (argv == 'logtime'):
            return logtime.main()
        elif (argv == 'logweather'):
            return logweather.main()
        elif (argv == 'logatis'):
            return logatis.main()

    try:
        sys.argv[1]
    except IndexError:
        runMain()
    else:
        runScripts(sys.argv[1])