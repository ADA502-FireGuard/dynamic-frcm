from frcm.datamodel.model import Location
import requests
import json

from frcm.weatherdata.client import LocationDataClient

class GeoCodingClient(LocationDataClient):

    # TODO: [FIR-34] Implement RestAPI methods. Requires the use of Kartverket's geocoding api.

    def __init__(self):
        pass

    def fetch_coordinates_from_address(self, address: str) -> Location:
        pass
    

    def fetch_coordinates_from_postcode(self, postcode: int) -> Location:
        pass