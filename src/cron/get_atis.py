import os
import json
import requests
import pandas as pd
import pprint
import datetime as dt


from parsed_atis import ParsedAtis

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


def round_seconds(obj: dt.datetime) -> dt.datetime:
    if obj.microsecond >= 500_000:
        obj += dt.timedelta(seconds=1)
    return obj.replace(microsecond=0)

def get_daystamp_name():
    local_time = dt.datetime.now()
    local_time_seconds = round_seconds(local_time)
    # includes hour, minute, seconds
    # return dt.datetime.strptime(str(utc_time_seconds), '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d-%H-%M-%S')
    return dt.datetime.strptime(str(local_time_seconds), '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d')


def process(atis_report: dict) -> pd.DataFrame:
    processed = []
    print('\n')
    pprint.pprint(atis_report)
    processed.append(atis_report)
    print('\n')
    return pd.DataFrame(processed)


if __name__ == '__main__':

    duh_path = os.path.normpath('~/Sites/gloomer/tmp/')
    abs_path = os.path.abspath(os.path.normpath('tmp/'))

    onlyfiles = [f for f in os.listdir(abs_path) if os.path.isfile(os.path.join(abs_path, f))]

    atis_reports = fetch(url=ATIS_URL)

    atis_report = ParsedAtis(atis_reports[0])
    parsed_atis = process(atis_report=atis_report.get_parsed_atis())

    proposed_file_name = f'atis_{AIRPORT_CODE}_{get_daystamp_name()}.csv'
    new_file_path = os.path.abspath(os.path.join(abs_path, proposed_file_name))
    print(f'proposed_file_name: {proposed_file_name}')


    if (proposed_file_name in onlyfiles):
        print('file already exists!')
        save_append(atis_reports=parsed_atis, path=new_file_path)
    else:
        print(f'new_file_path: {new_file_path}')
        save(atis_reports=atis_reports, path=new_file_path)