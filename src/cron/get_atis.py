import os
import re
import json
import string
import requests
import pandas as pd
import pprint
import datetime as dt
import time

AIRPORT_CODE = 'kdca'
ATIS_ENDPOINT = 'https://datis.clowd.io/api'
ATIS_URL = f'{ATIS_ENDPOINT}/{AIRPORT_CODE}'

landing_string = 'LNDG'
departure_string = 'DEPG'


def fetch(url: str) -> list:
    res = requests.get(url)
    return json.loads(res.content)


def split_sentences(str):
    regex = '(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s'
    result = re.split(regex, str)
    return result


def get_words(test_string):
    return re.sub('['+string.punctuation+']', '', test_string).split()

def get_runway_numbers(str):
    return re.findall(r'\d+\w*', str)

def get_runways(atis_sentences):
    landing_sentence = next(filter(lambda sentence: landing_string in sentence, atis_sentences), None)
    departure_sentence = next(filter(lambda sentence: departure_string in sentence, atis_sentences), None)
    landing_runways = None if landing_sentence == None else get_runway_numbers(landing_sentence)
    departure_runways = None if departure_sentence == None else get_runway_numbers(departure_sentence)

    landing_runway_primary = None if landing_sentence == None else landing_runways[0]
    landing_runway_secondary = None
    departure_runway_primary = None if departure_runways == None else departure_runways[0]
    departure_runway_secondary = None
    if (landing_runway_primary != None and len(landing_runways) >= 2):
        landing_runway_secondary = landing_runways[1]
    if (departure_runway_primary != None and len(departure_runways) >= 2):
        departure_runway_secondary = landing_runways[1]

    return {
        'landing_runway_primary': landing_runway_primary,
        'landing_runway_secondary': landing_runway_secondary,
        'departure_runway_primary': departure_runway_primary,
        'departure_runway_secondary': departure_runway_secondary
    }
    

def round_seconds(obj: dt.datetime) -> dt.datetime:
    if obj.microsecond >= 500_000:
        obj += dt.timedelta(seconds=1)
    return obj.replace(microsecond=0)


def get_time(atis_time):
    epoch = time.time()
    # local_ts = dt.datetime.fromtimestamp(epoch)
    # utc_ts = dt.datetime.utcfromtimestamp(epoch)
    atis_time_formatted = dt.datetime.strptime(str(atis_time), '%H%M%z')
    utc_ts = round_seconds(dt.datetime.utcnow())
    local_ts = dt.datetime.now()
    atis_datetime = utc_ts.replace(hour=atis_time_formatted.hour, minute=atis_time_formatted.minute, second=0, microsecond=0)
    atis_epoch = atis_datetime.timestamp()

    return {
        'local_ts': str(local_ts),
        'retrieved_utc': str(utc_ts),
        'retrieved_epoch': epoch,
        'atis_utc': str(atis_datetime),
        'atis_epoch': atis_epoch
    }


def process(atis_reports: list) -> pd.DataFrame:
    processed = []
    print('\n')
    for atis in atis_reports:
        datis = atis['datis']
        sentences = split_sentences(datis)

        atis_time = re.search('\d{4}Z', sentences[0]).group(0)
        time_values = get_time(atis_time)

        entry = {
            'iata_code': re.search('^[A-Z]+', sentences[0]).group(0),
            'icao_code': atis['airport'],
            'atis_icao': re.search(r'\b[A-Z]{1}\b', sentences[0]).group(0),
            'atis_time': atis_time,
            'atis_ts': time_values['atis_utc'],
            'retrieved_ts': time_values['retrieved_utc'],
            **get_runways(sentences),
            'atis': sentences
        }

        pprint.pprint(entry)

        processed.append(entry)
    print('\n')
    return pd.DataFrame(processed)


def save(atis_reports: pd.DataFrame, path: str) -> None:
    atis_reports.to_csv(path, index=False)


def round_seconds(obj: dt.datetime) -> dt.datetime:
    if obj.microsecond >= 500_000:
        obj += dt.timedelta(seconds=1)
    return obj.replace(microsecond=0)


def get_timestamp_name():
    # curr_timestamp = int(dt.datetime.timestamp(dt.datetime.now()))
    utc_time = dt.datetime.utcnow()
    utc_time_seconds = round_seconds(utc_time)
    return dt.datetime.strptime(str(utc_time_seconds), '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d-%H-%M-%S')


if __name__ == '__main__':
    atis_reports = fetch(url=ATIS_URL)
    atis_reports = process(atis_reports=atis_reports)
    timestamp_name = get_timestamp_name()
    path = os.path.normpath(f'~/Sites/gloomer/tmp/atis_{AIRPORT_CODE}_{timestamp_name}.csv')
    save(atis_reports=atis_reports, path=path)