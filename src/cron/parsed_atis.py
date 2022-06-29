import re
import datetime as dt
import pytz

LANDING_STRING = 'LNDG'
DEPARTURE_STRING = 'DEPG'

class ParsedAtis:

    def __init__(self, atis_report, timezone):
        datis = atis_report['datis']
        sentences = ParsedAtis.split_sentences(datis)
        self.atis_time = re.search('\d{4}Z', sentences[0]).group(0)
        self.iata_code = re.search('^[A-Z]+', sentences[0]).group(0)
        self.icao_code = atis_report['airport']
        self.atis_icao = re.search(r'\b[A-Z]{1}\b', sentences[0]).group(0)
        self.sentences = sentences
        self.timezone = timezone
        
        localized_datetime = self.get_localized_datetime()
        self.retrieved_ts = localized_datetime.strftime('%Y-%m-%dT%H:%M:%S%z')
        ts = ParsedAtis.get_time_datetime(self.atis_time)
        self.atis_ts = f'{ts.strftime("%Y-%m-%dT%H:%M")}Z'

        self.runways = None
        self.set_runways()

    def set_runways(self):
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

        self.runways = {
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
            'atis_ts': self.atis_ts,
            'retrieved_ts': self.retrieved_ts,
            **self.runways,
            'atis': self.sentences
        }
        return parsed_atis


    def get_localized_datetime(self):
        datetime_now = ParsedAtis.round_seconds(dt.datetime.now())
        localtime = pytz.timezone(self.timezone)
        return localtime.localize(datetime_now)


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
    
    @staticmethod
    def get_timezone_code():
        now = dt.datetime.utcnow()
        local_now = now.astimezone()
        local_tz = local_now.tzinfo
        return local_tz.tzname(local_now)
    
    @staticmethod
    def get_time_datetime(timestamp):
        # If the time difference betwen UTC now and UTC midnight is less than
        # the difference between UTC now the given timestamp, then the timestamp
        # occurred on the day before UTC now.
        utc_ts = ParsedAtis.round_seconds(dt.datetime.utcnow())
        formatted_ts = dt.datetime.strptime(str(timestamp), '%H%M%z')
        time_midnight = dt.datetime.strptime('00Z', '%H%z')
        time_now = dt.datetime.strptime(f'{utc_ts.hour}-{utc_ts.minute}Z', '%H-%M%z')
        now_midnight_diff = (time_now - time_midnight).total_seconds()
        now_to_ts_diff = (time_now - formatted_ts).total_seconds()

        if (now_to_ts_diff < 0):
            now_to_ts_diff = ((time_now + dt.timedelta(days=1)) - formatted_ts).total_seconds()

        ts_with_datetime = utc_ts.replace(
            hour=formatted_ts.hour, 
            minute=formatted_ts.minute, 
            second=0, 
            microsecond=0
        )

        is_same_day_ts = True if now_midnight_diff > now_to_ts_diff else False
        if (is_same_day_ts == False):
            ts_with_datetime -= dt.timedelta(days=1)
        
        return ts_with_datetime
    

