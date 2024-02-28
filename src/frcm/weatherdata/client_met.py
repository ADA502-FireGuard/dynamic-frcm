import requests
import datetime
import json
#import logging

# see .env.example.py in the root dir.
from decouple import config

from frcm.weatherdata.client import WeatherDataClient
from frcm.weatherdata.extractor import Extractor
from frcm.datamodel.model import Location, Observations, Forecast


class METClient(WeatherDataClient):

    def __init__(self, extractor: Extractor):

        self.forecast_endpoint = 'https://api.met.no/weatherapi/locationforecast/2.0/compact.json'

        self.observations_endpoint = 'https://frost.met.no/observations/v0.jsonld'
        self.sources_endpoint = 'https://frost.met.no/sources/v0.jsonld'

        self.MET_CLIENT_ID = config('MET_CLIENT_ID')
        self.MET_CLIENT_SECRET = config('MET_CLIENT_SECRET')

        self.extractor = extractor

    def send_met_request(self, parameters):

        try:
            header = {'User-Agent': 'DYNAMIC Firerisk Model'}

            response = requests.get(self.forecast_endpoint,
                                    headers=header,
                                    params=parameters,
                                    auth=(self.MET_CLIENT_ID, self.MET_CLIENT_SECRET))

            return response
        except Exception as other_err:
            # Logging.exception("Other-errors in get_nearest_station_id")
            print(f"Unexpected error: {other_err}")
            return "Error: Unexpected error"

    def fetch_forecast_raw(self, location: Location):

        try:
            parameters = {'lat': str(location.latitude),
                          'lon': str(location.longitude)
                          }

            response = self.send_met_request(parameters)

            return response
        except Exception as other_err:
            # Logging.exception("Other-errors in get_nearest_station_id")
            print(f"Unexpected error: {other_err}")
            return "Error: Unexpected error"

    def fetch_forecast(self, location: Location) -> Forecast:

        try:
            response = self.fetch_forecast_raw(location)

            forecast = self.extractor.extract_forecast(response.text)

            return forecast
        except Exception as other_err:
            # Logging.exception("Other-errors in get_nearest_station_id")
            print(f"Unexpected error: {other_err}")
            return "Error: Unexpected error"

    def send_frost_request(self, endpoint, parameters):

        try:
            response = requests.get(endpoint,
                                params=parameters,
                                auth=(self.MET_CLIENT_ID, self.MET_CLIENT_SECRET))

            return response
        except Exception as other_err:
            # Logging.exception("Other-errors in get_nearest_station_id")
            print(f"Unexpected error: {other_err}")
            return "Error: Unexpected error"

    def get_nearest_station_raw(self, location: Location):

        try:
            parameters = {
            'types': 'SensorSystem',
            'elements': 'air_temperature,relative_humidity,wind_speed',
            'geometry':  f'nearest(POINT({location.longitude} {location.latitude}))'}

            response = self.send_frost_request(self.sources_endpoint, parameters)

            return response
        except Exception as other_err:
            # Logging.exception("Other-errors in get_nearest_station_id")
            print(f"Unexpected error: {other_err}")
            return "Error: Unexpected error"

    def get_nearest_station_id(self, location: Location) -> str:
        
        try:
            # Fetch raw data from the nearest station
            frost_response = self.get_nearest_station_raw(location)
            frost_response_str = frost_response.text
            # Parse the JSON response
            station_response = json.loads(frost_response_str)
            # Extract the station ID
            station_id = station_response['data'][0]['id']
            return station_id
        except Exception as other_err:
            # Logging.exception("Other-errors in get_nearest_station_id")
            print(f"Unexpected error: {other_err}")
            return "Error: Unexpected error"

    @staticmethod
    def format_date(dt: datetime.datetime):

        return dt.strftime('%Y-%m-%d')

    @staticmethod
    def format_period(start: datetime.datetime, end: datetime.datetime):

        start_date = METClient.format_date(start)

        end_date = METClient.format_date(end)

        timeperiod = f'{start_date}/{end_date}'

        return timeperiod

    def fetch_observations_raw(self, source: str, start: datetime.datetime, end: datetime.datetime):
        
        try:
            time_period = METClient.format_period(start, end)

            print(f'Fetch observation : {time_period}')

            parameters = {'sources': source,
                          'referencetime': time_period,
                          'elements': 'air_temperature,relative_humidity,wind_speed'
                         }

            response = self.send_frost_request(self.observations_endpoint, parameters)

            return response
        except Exception as other_err:
            # Logging.exception("Other-errors in get_nearest_station_id")
            print(f"Unexpected error: {other_err}")
            return "Error: Unexpected error"

    def fetch_observations(self, location: Location, start: datetime.datetime, end: datetime.datetime) -> Observations:



        try:
#           print(location)
            station_id = self.get_nearest_station_id(location)

#           print(station_id)

            response = self.fetch_observations_raw(station_id, start, end)

#           print(response.text)

            observations = self.extractor.extract_observations(response.text, location)

            return observations
        except Exception as other_err:
            # Logging.exception("Other-errors in get_nearest_station_id")
            print(f"Unexpected error: {other_err}")
            return "Error: Unexpected error"
