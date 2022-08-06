"""
Main file.
"""
import os
from pprint import pprint
import sys
from geographiclib.geodesic import Geodesic
from cron import logtime, logweather, logatis
from utils import utils
from utils.definitions import ROOT_DIR
# import math
geod = Geodesic.WGS84
# import definitions


def map_function(config):
    """ mapping function which parses aircraft info """
    base_latitude = config['latitude']
    base_longitude = config['longitude']
    radius = config['radius']

    def mapper(plane):
        flight = None if 'flight' not in plane else plane['flight']
        latitude = None if 'lat' not in plane else plane['lat']
        longitude = None if 'lon' not in plane else plane['lon']
        track = None if 'track' not in plane else plane['track']
        altitude = None if 'altitude' not in plane else plane['altitude']
        speed = None if 'speed' not in plane else plane['speed']

        plane_info = {
            'hex': plane['hex']
        }
        if flight:
            plane_info['flight'] = flight
        if latitude:
            plane_info['latitude'] = latitude
        if longitude:
            plane_info['longitude'] = longitude
        if track:
            plane_info['track'] = track
        if altitude:
            plane_info['altitude'] = altitude
        if speed:
            plane_info['speed'] = speed

        if ('latitude' in plane_info and 'longitude' in plane_info):
            geo = geod.Inverse(
                base_latitude, base_longitude, plane_info['latitude'],
                plane_info['longitude']
            )

            distance_meters = geo['s12']

            if distance_meters < radius:
                plane_info['geo']  = geo
                plane_info['distance_meters'] = distance_meters

        return plane_info
    return mapper


def filter_format_aircraft(aircraft, adsb_config):
    """ formats and filters aircraft data based on configs """
    aircraft_with_data = list(filter(lambda plane: 'lat' in plane, aircraft))
    formatted_aircraft = list(map(map_function(adsb_config), aircraft_with_data))
    return list(filter(lambda plane: 'geo' in plane, formatted_aircraft))


def main():
    """ main script """
    print('Running aircraft locater.')
    config = utils.get_config()
    adsb_config = config['adsb']

    json_path = os.path.join(ROOT_DIR, 'tmp', '1658686085.json')
    aircraft_json = utils.open_json(json_path)
    aircraft = aircraft_json['aircraft']
    selected_aircraft = filter_format_aircraft(aircraft, adsb_config)

    print(f'{len(selected_aircraft)} nearby aircraft found.')

    for plane in filter_format_aircraft(aircraft, adsb_config):
        distance_meters = plane['geo']['s12']

        print('\n')
        pprint(plane)
        print(f'The distance is {distance_meters:.3f} m')


if __name__ == '__main__':
    def run_main():
        """ main script """
        return main()

    def run_scripts(argv):
        """ other scripts """
        script = utils.noop

        if argv == 'logtime':
            script = logtime.main
        elif argv == 'logweather':
            script = logweather.main
        elif argv == 'logatis':
            script = logatis.main

        script()

    try:
        sys.argv[1]
    except IndexError:
        run_main()
    else:
        run_scripts(sys.argv[1])
