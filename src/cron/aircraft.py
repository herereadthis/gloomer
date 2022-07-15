import os
import json
import requests
from pprint import pprint
import toml

import utils


def fetch(url: str) -> list:
    res = requests.get(url)
    return json.loads(res.content)


if __name__ == '__main__':
    config = toml.load(utils.get_config_file_path())
    adsb_config = config['adsb']
    adsb_latitude = adsb_config['latitude']
    adsb_longitude = adsb_config['longitude']
    adsb_radius = adsb_config['radius']

    properties = {
        'latidude': adsb_latitude,
        'longitude': adsb_longitude,
        'radius': adsb_radius,
    }

    pprint(properties)


    # dirname = os.path.dirname(__file__)
    # filename = os.path.join(dirname, 'your relative path to the file')
    # foo = os.path.join(dirname, '../../tmp/1657290545.json')

    # print(dirname)
    # print(filename)
    # print(foo)

    # json_dump = fetch(url=foo)



    print(os.path.join(os.path.dirname(__file__), '..', '..', 'tmp', '1657290545.json'))
    # results in C:\projects\relative_path\processes\..\data\mydata.json

    print(os.path.realpath(os.path.join(os.path.dirname(__file__), '..', '..', 'tmp', '1657290545.json')))
    # results in C:\projects\relative_path\data\mydata.json
    # print(json_dump)