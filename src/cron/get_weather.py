import os
import xml.etree.ElementTree as ET
import pandas as pd
from pprint import pprint
import toml

import utils
from parsed_weather import ParsedWeather
from data_file import DataFile


def save(reports: pd.DataFrame, path: str) -> None:
    reports.to_csv(path, index=False)


def save_append(reports: pd.DataFrame, path: str) -> None:
    reports.to_csv(path, index=False, mode='a', header=False)


def process_weather(parsed_weather) -> pd.DataFrame:
    pprint(parsed_weather)
    return pd.DataFrame([parsed_weather])


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
    base_file_name = f'weather_{airport_icao}'


    parsed_weather = ParsedWeather(airport_icao, airport_timezone)
    weather_dataframe = process_weather(parsed_weather.weather_report)

    data_file = DataFile(
        log_path = get_log_path(config),
        base_file_name = f'weather_{airport_icao}',
        report = parsed_weather.weather_report
    )
    print(data_file)

    only_files = [f for f in os.listdir(log_path) if os.path.isfile(os.path.join(log_path, f))]


    proposed_file_name = f'weather_{airport_icao}_{utils.get_daystamp_name()}.csv'
    file_path = os.path.abspath(os.path.join(log_path, proposed_file_name))
    print(proposed_file_name)
    print(file_path)

    if (proposed_file_name in only_files):
        last_observation_ts = get_last_entry_cell(file_path, 'observation_ts')
        current_observation_ts = weather_dataframe.loc[0, 'observation_ts']
        if (last_observation_ts == current_observation_ts):
            print('last report already recorded!')
        else:
            print('adding new report to existing file!')
            save_append(reports=weather_dataframe, path=file_path)
    else:
        print(f'new_file_path: {file_path}')
        save(reports=weather_dataframe, path=file_path)
