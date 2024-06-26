import json
import dateutil.parser
import numpy as np

from frcm.weatherdata.extractor import Extractor
from frcm.datamodel.model import *


class METExtractor(Extractor):

    def extract_observations(self, frost_response_str: str, location: Location) -> Observations:

        frost_response = json.loads(frost_response_str)
        data_list = frost_response['data']

        weatherdatapoints = list()

        source_id = None

        if len(data_list) > 1:

            source_id = data_list[0]['sourceId']

            for data in data_list:

                reference_time = dateutil.parser.parse(data['referenceTime'])
                station_observations = data['observations']

                temperature = np.nan
                relative_humidity = np.nan
                wind_speed = np.nan

                for station_observation in station_observations:

                    # string to datatime object required
                    timestamp = reference_time # assume that observations have the same time stamp

                    elementId =  station_observation['elementId']

                    match elementId:
                        case "air_temperature":
                            temperature = station_observation['value']
                        case "relative_humidity":
                            relative_humidity = station_observation['value']
                        case "wind_speed":
                            wind_speed = station_observation['value']
                        case _:
                            temperature = 10000     # OK to leave default case empty?

                wd_point = WeatherDataPoint(temperature=temperature,
                                            humidity=relative_humidity,
                                            wind_speed=wind_speed,
                                            timestamp=timestamp
                                            )

                weatherdatapoints.append(wd_point)

        observations = Observations(source=source_id, location=location,data=weatherdatapoints)

        return observations

    def extract_forecast(self, met_response_str: str) -> Forecast:

        met_response = json.loads(met_response_str)

        coordinates = met_response['geometry']['coordinates']

        latitude = coordinates[1]
        longitude = coordinates[0]

        location = Location(latitude=latitude, longitude=longitude)

        timeseries = met_response['properties']['timeseries']

        weatherdatapoints = list()

        for forecast in timeseries:

            timestamp = dateutil.parser.parse(forecast['time'])

            details = forecast['data']['instant']['details']

            temperature = details['air_temperature']
            humidity = details['relative_humidity']
            wind_speed = details['wind_speed']

            wd_point = WeatherDataPoint(temperature=temperature,
                                        humidity=humidity,
                                        wind_speed=wind_speed,
                                        timestamp=timestamp)

            weatherdatapoints.append(wd_point)

        forecast = Forecast(location=location,data=weatherdatapoints)

        return forecast

    def extract_weatherdata(self, frost_response: str, met_response: str, location: Location):

        observations = self.extract_observations(frost_response, location)

        forecast = self.extract_forecast(met_response)

        frost_response_json = json.loads(frost_response)
        frost_response_created_at = frost_response_json['createdAt']

        created = dateutil.parser.parse(timestr=frost_response_created_at, yearfirst=True)

        weather_data = WeatherData(created=created,
                                   observations=observations,
                                   forecast=forecast)

        return weather_data
