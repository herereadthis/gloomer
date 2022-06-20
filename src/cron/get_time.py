import os
from pprint import pprint
import toml

import utils

def save(file_path, new_line):
    with open(file_path, 'w') as fp:
        fp.write(new_line)

def save_append(file_path, new_line):
    with open(file_path, 'a') as fp:
        fp.write('\n')
        fp.write(new_line)


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

    only_files = [f for f in os.listdir(log_path) if os.path.isfile(os.path.join(log_path, f))]

    utc_datetime = utils.get_datetime_name()
    new_line = f'UTC date time: {utc_datetime}'

    proposed_file_name = f'cron_sample_{utils.get_daystamp_name()}.txt'
    file_path = os.path.abspath(os.path.join(log_path, proposed_file_name))
    print(f'proposed_file_name: {proposed_file_name}')

    if (proposed_file_name in only_files):
        print('file already exists!')
        print(new_line)
        save_append(file_path, new_line)
    else:
        print(f'new_file_path: {file_path}')
        print(new_line)
        save(file_path, new_line)