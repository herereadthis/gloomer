import os
import datetime as dt
from sys import platform
import requests
import json
import toml

from utils.definitions import ROOT_DIR

def fetch_json(url: str) -> list:
    res = requests.get(url)
    return json.loads(res.content)


def open_json(json_path):
    f = open(json_path)
    return json.load(f)


def get_config_file_path():
    # dir_path = os.path.dirname(os.path.realpath(__file__))
    # gloomer_path = dir_path.split('src')
    # config_file_path = os.path.join(gloomer_path[0], 'config.toml')
    config_file_path = os.path.join(ROOT_DIR, 'config.toml')

    try:
        assert (os.path.isfile(config_file_path)), 'config.toml file missing!'
    except Exception as e:
        print(e)
        exit()
    
    return config_file_path


def get_config():
    config_file_path = os.path.join(ROOT_DIR, 'config.toml')

    try:
        assert (os.path.isfile(config_file_path)), 'config.toml file missing!'
    except Exception as e:
        print(e)
        exit()
    
    return toml.load(config_file_path)


def get_user_root():
    supported_platforms = ['linux', 'darwin']
    
    try:
        assert (platform in supported_platforms), 'Unsupported OS!'
    except Exception as e:
        print(e)
        exit()
    
    home_dir = ''
    if (platform == 'linux'):
        home_dir = '/home'
    elif (platform == 'darwin'):
        home_dir = '/Users'
    
    user_root = os.getlogin()
    return f'{home_dir}/{user_root}'


def round_seconds(obj: dt.datetime) -> dt.datetime:
    if obj.microsecond >= 500_000:
        obj += dt.timedelta(seconds=1)
    return obj.replace(microsecond=0)


def get_datetime_name():
    utc_time = dt.datetime.utcnow()
    utc_time_seconds = round_seconds(utc_time)
    return dt.datetime.strptime(str(utc_time_seconds), '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d-%H-%M-%S')


def get_daystamp_name():
    local_time = dt.datetime.now()
    local_time_seconds = round_seconds(local_time)
    return dt.datetime.strptime(str(local_time_seconds), '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d')