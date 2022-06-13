import os
import re
import json
import string
import requests
import pandas as pd
import datetime as dt

AIRPORT_CODE = 'kdca'
ATIS_ENDPOINT = 'https://datis.clowd.io/api'
ATIS_URL = f'{ATIS_ENDPOINT}/{AIRPORT_CODE}'


def fetch(url: str) -> list:
    res = requests.get(url)
    return json.loads(res.content)


def split_sentences(str):
    regex = '(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s'
    result = re.split(regex, str)
    return result


def get_words(test_string):
    return re.sub('['+string.punctuation+']', '', test_string).split()


def process(atis_reports: list) -> pd.DataFrame:
    processed = []
    for atis in atis_reports:

        datis = atis['datis']
        print('\n')
        print(datis)
        print('\n')
        sentences = split_sentences(datis)
        first_sentence_words = get_words(sentences[0])
        for word in first_sentence_words:
            print(word)
        for sentence in sentences:
            print(sentence)


        processed.append({
            'airport_iata': first_sentence_words[0],
            'airport_icao': atis['airport'],
            # 'type': atis['type'],
            'icao': first_sentence_words[3],
            'time': first_sentence_words[4],
            'datis': atis['datis'],
        })
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