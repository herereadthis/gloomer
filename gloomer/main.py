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
    pprint(aircraft)
    print(len(aircraft))

    for plane in aircraft:



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