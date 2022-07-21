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
    print('aslkdjfhlaskdjfh')
    print('aslkdjfhlaskdjfh')
    print('aslkdjfhlaskdjfh')
    print('aslkdjfhlaskdjfh')
    pprint(config)


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

        print(plane_info)

        if ('latitude' in plane_info and 'longitude' in plane_info):
            geo = geod.Inverse(base_latitude, base_longitude, plane_info['latitude'], plane_info['longitude'])

            distance_meters = geo['s12']

            if (distance_meters < radius):
                plane_info['geo']  = geo
        
        return plane_info
    return mapper


def leftFn(foo):
    def rightFn(bar):
        print(f'{foo}, {bar}') 
    return rightFn

# leftFn('foo')('bar')


def main():
    config = toml.load(utils.get_config_file_path())
    adsb_config = config['adsb']
    base_latitude = adsb_config['latitude']
    base_longitude = adsb_config['longitude']
    radius = adsb_config['radius']

    # json_dump = os.path.join(ROOT_DIR, 'tmp', '1657319464.json')
    json_dump = os.path.join(ROOT_DIR, 'tmp', '1657322477.json')
    # json_dump = os.path.join(ROOT_DIR, 'tmp', '1657292525.json')
    print(json_dump)
    f = open(json_dump)

    # aircraft_json = fetch(url=json_dump)
    aircraft_json = json.load(f)
    aircraft = aircraft_json['aircraft']

    aircraft_with_data = list(filter(filter_function, aircraft))
    # pprint(aircraft_with_data)
    formatted_aircraft = list(map(map_function(adsb_config), aircraft_with_data))



    # pprint(formatted_aircraft)



    for plane in formatted_aircraft:
        if ('geo' in plane):
            distance_meters = plane['geo']['s12']

            if (distance_meters < radius):
                print('\n')
                print(plane)
                print("The distance is {:.3f} m.".format(distance_meters))




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