import os
import datetime as dt
from sys import platform

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