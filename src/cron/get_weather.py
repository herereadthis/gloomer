import os
import toml

import utils
from parsed_weather import ParsedWeather
from data_file import DataFile


def get_log_path(config):
    user_root = utils.get_user_root()
    log_dir = config['atis']['log_directory']
    log_path = f'{user_root}/{log_dir}'

    if (os.path.exists(log_path) == False):
        os.makedirs(log_path)
    
    return log_path


if __name__ == '__main__':
    config = toml.load(utils.get_config_file_path())
    airport_icao = config['weather']['airport_icao']
    airport_timezone = config['weather']['timezone']

    parsed_weather = ParsedWeather(airport_icao, airport_timezone)

    data_file = DataFile(
        log_path = get_log_path(config),
        base_file_name = f'weather_{airport_icao}',
        report = parsed_weather.weather_report,
        unique_key = 'observation_ts'
    )
    print(data_file)
    data_file.save_data()
