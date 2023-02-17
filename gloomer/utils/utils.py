import os
import datetime as dt
from sys import platform
import json
import requests
import sys
import toml

from utils.definitions import ROOT_DIR


def left_fn(left_param):
    """
    demo of function that returns a function
    left_fn('left_arg')('right_arg')
    """
    def right_fn(right_param):
        print(f'{left_param}, {right_param}')
    return right_fn


def noop():
    """ noop function """
    pass

def fetch_json(url: str) -> list:
    """ fetches json """
    res = requests.get(url)
    return json.loads(res.content)


def open_json(json_path):
    """ opens json from static file located in some directory """
    the_stuff = open(json_path)
    return json.load(the_stuff)


# def get_config_file_path():
#     """ get file path of the config file """
#     # dir_path = os.path.dirname(os.path.realpath(__file__))
#     # gloomer_path = dir_path.split('src')
#     # config_file_path = os.path.join(gloomer_path[0], 'config.toml')
#     config_file_path = os.path.join(ROOT_DIR, 'config.toml')

#     try:
#         assert (os.path.isfile(config_file_path)), 'config.toml file missing!'
#     except Exception as err:
#         print(err)
#         sys.exit()

#     return config_file_path


def get_config():
    """ get file path of the config file """
    config_file_path = os.path.join(ROOT_DIR, 'config.toml')

    try:
        assert (os.path.isfile(config_file_path)), 'config.toml file missing!'
    except Exception as err:
        print(err)
        sys.exit()

    return toml.load(config_file_path)


def get_user_root():
    """ get the root directory for the user running this function """
    supported_platforms = ['linux', 'darwin']

    try:
        assert (platform in supported_platforms), 'Unsupported OS!'
    except Exception as err:
        print(err)
        sys.exit()

    result = ''
    if platform == 'linux':
        home_dir = '/home'
        user_root = os.getlogin()
        result = f'{home_dir}/{user_root}'
    elif platform == 'darwin':
        result = os.path.expanduser('~')

    return result


def round_seconds(obj: dt.datetime) -> dt.datetime:
    """ rounds time microseconds to seconds """
    if obj.microsecond >= 500_000:
        obj += dt.timedelta(seconds=1)
    return obj.replace(microsecond=0)


def get_datetime_name():
    """ get formatted datetime to be used as a name """
    utc_time = dt.datetime.utcnow()
    utc_time_seconds = round_seconds(utc_time)
    return dt.datetime.strptime(
        str(utc_time_seconds), '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d-%H-%M-%S'
    )


def get_daystamp_name():
    """ get just the day from a datetime """
    local_time = dt.datetime.now()
    local_time_seconds = round_seconds(local_time)
    return dt.datetime.strptime(str(local_time_seconds), '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d')
