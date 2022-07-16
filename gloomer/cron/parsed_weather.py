import xml.etree.ElementTree as ET
import requests
from pprint import pprint
import re
import datetime as dt
import pytz
from pprint import pprint

WEATHER_URI = 'https://w1.weather.gov/xml/current_obs'

class ParsedWeather:

    def __init__(self, icao, timezone):
        self.icao = icao
        self.timezone = timezone
        self.url = f'{WEATHER_URI}/{icao.upper()}.xml'
    
    @property
    def weather_report(self):
        response = requests.get(self.url)
        root = ET.fromstring(response.content)
        get_datetime_string = ParsedWeather.get_datetime_string
        get_tag_value = ParsedWeather.get_tag_value

        observation_time_rfc822 = get_tag_value(root, 'observation_time_rfc822')
        formatted_ts = dt.datetime.strptime(observation_time_rfc822, '%a, %d %b %Y %H:%M:%S %z')

        localized_datetime = self.get_localized_datetime()

        weather_report = {
            'observation_ts': get_datetime_string(formatted_ts),
            'retrieved_ts': get_datetime_string(localized_datetime),
            'weather': get_tag_value(root, 'weather'),
            'temp_f': get_tag_value(root, 'temp_f'),
            'temp_c': get_tag_value(root, 'temp_c'),
            'relative_humidity': get_tag_value(root, 'relative_humidity'),
            'wind_dir': get_tag_value(root, 'wind_dir'),
            'wind_degrees': get_tag_value(root, 'wind_degrees'),
            'wind_mph': get_tag_value(root, 'wind_mph'),
            'wind_kt': get_tag_value(root, 'wind_kt'),
            'pressure_mb': get_tag_value(root, 'pressure_mb'),
            'pressure_in': get_tag_value(root, 'pressure_in'),
            'dewpoint_f': get_tag_value(root, 'dewpoint_f'),
            'dewpoint_c': get_tag_value(root, 'dewpoint_c'),
            'visibility_mi': get_tag_value(root, 'visibility_mi'),
            'pressure_in': get_tag_value(root, 'pressure_in')
        }
        return weather_report 


    def get_localized_datetime(self):
        datetime_now = ParsedWeather.round_seconds(dt.datetime.now())
        localtime = pytz.timezone(self.timezone)
        return localtime.localize(datetime_now)

    @staticmethod
    def get_datetime_string(ts):
        return ts.strftime('%Y-%m-%dT%H:%M:%S%z')

    @staticmethod
    def get_tag_value(root, loc):
        text = root.find(f'.//{loc}').text.strip()
        # from https://www.regextester.com/104184
        regex = '^-?([0]{1}\.{1}[0-9]+|[1-9]{1}[0-9]*\.{1}[0-9]+|[0-9]+|0)$'
        if re.match(regex, text) == None:
            result = text
        else:
            result = float(text)
        return result

    @staticmethod
    def round_seconds(obj: dt.datetime) -> dt.datetime:
        if obj.microsecond >= 500_000:
            obj += dt.timedelta(seconds=1)
        return obj.replace(microsecond=0)
