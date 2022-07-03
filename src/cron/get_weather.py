import os
import xml.etree.ElementTree as ET
import pandas as pd
from pprint import pprint
import toml
import re
import datetime as dt

import utils
from parsed_atis import ParsedAtis
from parsed_weather import ParsedWeather


def save(atis_reports: pd.DataFrame, path: str) -> None:
    atis_reports.to_csv(path, index=False)


def save_append(atis_reports: pd.DataFrame, path: str) -> None:
    atis_reports.to_csv(path, index=False, mode='a', header=False)


def process_atis(config) -> pd.DataFrame:
    atis_config = config['atis']
    endpoint = atis_config['endpoint']
    airport_icao = atis_config['airport_icao']
    timezone = atis_config['timezone']
    atis_url = f'{endpoint}/{airport_icao}'
    atis_reports = fetch(url=atis_url)
    atis_report = ParsedAtis(atis_reports[0], timezone)
    parsed_atis = atis_report.get_parsed_atis()

    print('\n')
    pprint(parsed_atis)
    print('\n')

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
    config = toml.load(utils.get_config_file_path())
    log_path = get_log_path(config)
    airport_icao = config['weather']['airport_icao']
    airport_timezone = config['weather']['timezone']

    only_files = [f for f in os.listdir(log_path) if os.path.isfile(os.path.join(log_path, f))]

    parsedWeather = ParsedWeather(airport_icao, airport_timezone)

    pprint(parsedWeather.weather_report)

    

    # atis_dataframe = process_atis(config)

    # proposed_file_name = f'atis_{airport_icao}_{utils.get_daystamp_name()}.csv'
    # file_path = os.path.abspath(os.path.join(log_path, proposed_file_name))
    # print(f'proposed_file_name: {proposed_file_name}')

    # if (proposed_file_name in only_files):
    #     last_icao = get_last_entry_cell(file_path, 'atis_icao')
    #     current_icao = atis_dataframe.loc[0, 'atis_icao']
    #     if (last_icao == current_icao):
    #         print('last atis already recorded!')
    #     else:
    #         print('adding new atis to existing file!')
    #         save_append(atis_reports=atis_dataframe, path=file_path)
    # else:
    #     print(f'new_file_path: {file_path}')
    #     save(atis_reports=atis_dataframe, path=file_path)