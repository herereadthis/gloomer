import time
import datetime as dt
import os.path

TEMP_DIRECTORY = '../../tmp'

def get_epoch_milliseconds():
    return int(round(time.time() * 1000))


def get_time_milliseconds(*args):
    proposed_time = dt.datetime(*args)
    epoch = dt.datetime.utcfromtimestamp(0)
    return round((proposed_time - epoch).total_seconds() * 1000)


def get_time_diff_milliseconds(*args):
    current_time = get_epoch_milliseconds()
    future_time = get_time_milliseconds(*args)
    return future_time - current_time

def round_seconds(obj: dt.datetime) -> dt.datetime:
    if obj.microsecond >= 500_000:
        obj += dt.timedelta(seconds=1)
    return obj.replace(microsecond=0)

def create_temp_directory():
    # Path 
    path = '../../tmp'
        
    # Check whether the  
    # specified path is an 
    # existing directory or not 
    isdir = os.path.isdir(TEMP_DIRECTORY) 
    print(isdir) 
    if (isdir == False):
        os.mkdir(TEMP_DIRECTORY)


if __name__ == '__main__':
    create_temp_directory()
    diff = get_time_diff_milliseconds(2022, 6, 8, 2, 1, 0)
    print(diff)

    secs = diff / 1000
    print(secs)

    foo = dt.datetime.now()
    baz = round_seconds(foo)
    print(str(baz))
    bar = dt.datetime.strptime(str(baz), '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d-%H-%M-%S')
    filename = f'{TEMP_DIRECTORY}/{bar}.json'

    with open(filename, 'w') as f:
        f.write('insert json here')

    print(bar)
    print(filename)