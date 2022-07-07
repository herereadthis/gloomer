import os
import json
import requests
from pprint import pprint
import toml

import utils
from parsed_atis import ParsedAtis
from data_file import DataFile


def fetch(url: str) -> list:
    res = requests.get(url)
    return json.loads(res.content)


def get_log_path(config):
    user_root = utils.get_user_root()
    log_dir = config['atis']['log_directory']
    log_path = f'{user_root}/{log_dir}'

    if (os.path.exists(log_path) == False):
        os.makedirs(log_path)
    
    return log_path


if __name__ == '__main__':
    config = toml.load(utils.get_config_file_path())
    atis_config = config['atis']
    airport_icao = atis_config['airport_icao']
    atis_url = atis_config['endpoint'] + '/' + airport_icao
    atis_reports = fetch(url=atis_url)
    atis_report = ParsedAtis(atis_reports[0], atis_config['timezone'])
    parsed_atis = atis_report.get_parsed_atis()

    print('\n')
    pprint(parsed_atis)
    print('\n')
    
    data_file = DataFile(
        log_path = get_log_path(config),
        base_file_name = f'atis_{airport_icao}',
        report = parsed_atis,
        unique_key = 'atis_icao'
    )
    data_file.save_data()
