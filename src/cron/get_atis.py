import os
import json
import requests
import pandas as pd
import datetime as dt
import configparser

import utils
from parsed_atis import ParsedAtis

config = configparser.ConfigParser()
config.read('../../config.ini')

AIRPORT_CODE = 'kdca'
ATIS_ENDPOINT = 'https://datis.clowd.io/api'
ATIS_URL = f'{ATIS_ENDPOINT}/{AIRPORT_CODE}'

landing_string = 'LNDG'
departure_string = 'DEPG'


def fetch(url: str) -> list:
    res = requests.get(url)
    return json.loads(res.content)


def save(atis_reports: pd.DataFrame, path: str) -> None:
    atis_reports.to_csv(path, index=False)


def save_append(atis_reports: pd.DataFrame, path: str) -> None:
    atis_reports.to_csv(path, index=False, mode='a', header=False)


def process_atis() -> pd.DataFrame:
    atis_reports = fetch(url=ATIS_URL)
    atis_report = ParsedAtis(atis_reports[0])
    parsed_atis = atis_report.get_parsed_atis()
    return pd.DataFrame([parsed_atis])


def get_last_entry_cell(file_path, cell_name) -> str:
    df = pd.read_csv(file_path)
    return df.loc[df.index[-1],cell_name]


def get_log_path(config):
    user_root = utils.get_user_root()
    log_dir = config['atis']['log_directory']
    log_path = f'{user_root}/{log_dir}'

    if (os.path.exists(log_path) == False):
        os.makedirs(log_path)
    
    return log_path


if __name__ == '__main__':
    config = configparser.ConfigParser()
    config.read(utils.get_config_file_path())
    log_path = get_log_path(config)

    only_files = [f for f in os.listdir(log_path) if os.path.isfile(os.path.join(log_path, f))]

    atis_dataframe = process_atis()

    proposed_file_name = f'atis_{AIRPORT_CODE}_{utils.get_daystamp_name()}.csv'
    file_path = os.path.abspath(os.path.join(log_path, proposed_file_name))
    print(f'proposed_file_name: {proposed_file_name}')

    if (proposed_file_name in only_files):
        last_icao = get_last_entry_cell(file_path, 'atis_icao')
        current_icao = atis_dataframe.loc[0, 'atis_icao']
        if (last_icao == current_icao):
            print('last atis already recorded!')
        else:
            print('adding new atis to existing file!')
            save_append(atis_reports=atis_dataframe, path=file_path)
    else:
        print(f'new_file_path: {file_path}')
        save(atis_reports=atis_dataframe, path=file_path)