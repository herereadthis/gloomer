import os

from utils import utils
from cron.parsed_weather import ParsedWeather
from cron.data_file import DataFile


def get_log_path(config):
    user_root = utils.get_user_root()
    log_dir = config['atis']['log_directory']
    log_path = f'{user_root}/{log_dir}'

    if (os.path.exists(log_path) == False):
        os.makedirs(log_path)
    
    return log_path

def main():
    config = utils.get_config()
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


if __name__ == '__main__':
    main()
