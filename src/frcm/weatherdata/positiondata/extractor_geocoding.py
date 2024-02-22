import json
from frcm.datamodel.model import Location
import numpy as np

from frcm.weatherdata.extractor import LocationExtractor

class GeoCodingExtractor(LocationExtractor):
    
    # TODO: [FIR-34] Implement RestAPI methods. Requires the use of Kartverket's geocoding api.

    def __init__(self):
        pass

    def extract_coordinates(self, data: str) -> Location:
        pass