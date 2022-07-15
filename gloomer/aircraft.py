import os
import json
import requests
from pprint import pprint

from yum import utils

from definitions import ROOT_DIR


def fetch(url: str) -> list:
    res = requests.get(url)
    return json.loads(res.content)

if __name__ == '__main__':
    print('hello world')

    json_dump = os.path.join(ROOT_DIR, 'tmp', '1657290545.json')
    print(json_dump)
    print(json_dump)
    f = open(json_dump)

    # aircraft_json = fetch(url=json_dump)
    aircraft_json = json.load(f)
    pprint(aircraft_json)