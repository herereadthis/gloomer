import re
import pandas as pd
from pprint import pprint
import datetime as dt
import time


LANDING_STRING = 'LNDG'
DEPARTURE_STRING = 'DEPG'

class ParsedAtis:

    def __init__(self, atis_report):
        datis = atis_report['datis']
        sentences = ParsedAtis.split_sentences(datis)
        self.atis_time = re.search('\d{4}Z', sentences[0]).group(0)
        self.iata_code = re.search('^[A-Z]+', sentences[0]).group(0)
        self.icao_code = atis_report['airport']
        self.atis_icao = re.search(r'\b[A-Z]{1}\b', sentences[0]).group(0)
        self.sentences = sentences

    @property
    def time_values(self):
        epoch = time.time()
        # local_ts = dt.datetime.fromtimestamp(epoch)
        # utc_ts = dt.datetime.utcfromtimestamp(epoch)
        atis_time_formatted = dt.datetime.strptime(str(self.atis_time), '%H%M%z')
        utc_ts = ParsedAtis.round_seconds(dt.datetime.utcnow())
        # foo_ts = dt.datetime.now(dt.timezone.utc)

        print(f'atis_time_formatted: {atis_time_formatted.isoformat()}')
        print(f'utc_ts: {utc_ts.isoformat()}')
        # print(f'foo_ts: {foo_ts.isoformat()}')

        now = dt.datetime.now()
        local_now = now.astimezone()
        local_tz = local_now.tzinfo
        local_tzname = local_tz.tzname(local_now)
        print(local_tzname)

        local_ts = dt.datetime.now()
        atis_datetime = utc_ts.replace(
            hour=atis_time_formatted.hour, 
            minute=atis_time_formatted.minute, 
            second=0, 
            microsecond=0
        )

        return {
            'local_ts': str(local_ts),
            'retrieved_utc': str(utc_ts),
            'retrieved_epoch': epoch,
            'atis_utc': str(atis_datetime),
            'atis_epoch': atis_datetime.timestamp()
        }

    @property
    def runways(self):
        landing_sentence = next(filter(lambda sentence: LANDING_STRING in sentence, self.sentences), None)
        departure_sentence = next(filter(lambda sentence: DEPARTURE_STRING in sentence, self.sentences), None)
        landing_runways = None if landing_sentence == None else ParsedAtis.get_runway_numbers(landing_sentence)
        departure_runways = None if departure_sentence == None else ParsedAtis.get_runway_numbers(departure_sentence)

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
    
    def get_parsed_atis(self):
        parsed_atis = {
            'iata_code': self.iata_code,
            'icao_code': self.icao_code,
            'atis_icao': self.atis_icao,
            'atis_time': self.atis_time,
            'atis_ts': self.time_values['atis_utc'],
            'retrieved_ts': self.time_values['retrieved_utc'],
            **self.runways,
            'atis': self.sentences
        }
        print('\n')
        pprint(parsed_atis)
        print('\n')
        return parsed_atis

    @staticmethod
    def get_runway_numbers(str):
        return re.findall(r'\d+\w*', str)

    @staticmethod
    def split_sentences(str):
        regex = '(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s'
        result = re.split(regex, str)
        return result

    @staticmethod
    def round_seconds(obj: dt.datetime) -> dt.datetime:
        if obj.microsecond >= 500_000:
            obj += dt.timedelta(seconds=1)
        return obj.replace(microsecond=0)
