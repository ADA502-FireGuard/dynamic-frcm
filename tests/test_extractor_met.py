import os
import sys

current = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src"))
sys.path.insert(0, current)

import unittest
import json

from frcm.weatherdata import extractor_met as METExtractor

import sampledata.met_sample_forecast
import sampledata.frost_sample_observation

from frcm.datamodel.model import Location


class TestUtil(unittest.TestCase):

    def setUp(self):

        self.location_obs = Location(latitude=60.383, longitude=5.3327)
        self.location_fct = Location(latitude=60.3915, longitude=5.3199)

        self.met_extractor = METExtractor()

        self.met_sample_forecast_str = json.dumps(sampledata.met_sample_forecast.met_sample_forecast)
        self.frost_sample_observation_str = json.dumps(sampledata.frost_sample_observation.frost_sample_observation)

    def test_extractor_obs(self):

        observations = self.met_extractor.extract_observations(self.frost_sample_observation_str,
                                                               self.location_obs)
        print(observations)

        self.assertEqual(len(observations.data), 24)

    def test_extractor_fct(self):

        forecast = self.met_extractor.extract_forecast(self.met_sample_forecast_str)

        print(forecast)

        self.assertEqual(len(forecast.data), 85)

    def test_extractor_weatherdata(self):

        weatherdata = self.met_extractor.extract_weatherdata(frost_response=self.frost_sample_observation_str,
                                                             met_response=self.met_sample_forecast_str,
                                                             location=self.location_obs)

        self.assertEqual(self.location_obs, weatherdata.observations.location)
        self.assertEqual(self.location_fct, weatherdata.forecast.location)

        self.assertEqual(len(weatherdata.observations.data), 24)
        self.assertEqual(len(weatherdata.forecast.data), 85)

if __name__ == '__main__':
    unittest.main()




