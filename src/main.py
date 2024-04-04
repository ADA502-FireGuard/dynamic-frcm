from fastapi import FastAPI, Response, status
from fastapi import FastAPI, Response, status
from frcm.weatherdata.utils import weatherdata_parse
from frcm.datamodel.model import WeatherDataPoint
from frcm.frcapi import FireRiskAPI
from frcm.weatherdata.client_met import METClient
from frcm.weatherdata.extractor_met import METExtractor
from frcm.weatherdata.positiondata.client_geocoding import GeoCodingClient
from frcm.weatherdata.positiondata.extractor_geocoding import GeoCodingExtractor
from frcm.logic.logic_handler import LogicHandler
from frcm.datamodel.model import Location
import datetime
import dateutil.parser
import time
import threading

# sample code illustrating how to use the Fire Risk Computation API (FRCAPI)
logic_handler: LogicHandler = LogicHandler()
if __name__ == "__main__":
    
    # Init LogicHandler object.

    """
        user -> restapi (thread) -> waiting_list LogicHandler 
        -> Database
        -> GPS? ->  METClient
        -> Addresse / anna ->  GeoClient -> METClient
    """


# Start of RestAPI implementation. Below is defined all the paths that are used to access the FireGuard Cloud Service.
app = FastAPI()

# Root. Returns a simple message to confirm that the user can reach the FireGuard Cloud Service.
@app.get("/fireguard")
async def root():
    return {"message": "FireGuard Cloud Service"}


# Authenticates user. Unnessecary?
@app.get("/fireguard/authenticate")
async def authenticate ():
    pass


# Default for services selection. Returns JSON containing info on available services, input variables required and return values.
@app.get("/fireguard/services")
async def services ():
    return {
        "message": "FireGuard services",
        "rawdata": {
            "temp": "float", 
            "temp_forecast": "float",
            "humidity": "float",
            "humidity_forecast": "float",
            "wind_speed": "float",
            "wind_speed_forecast": "float",
            "timestamp": "str",
            "timestamp_forecast": "str",
            "return": ""
        },
        "area": {
            "gps": {
                "lon": "float", 
                "lat": "float",
                "days (optional, default = 1, minimum = 1)": "int",
                "return": ""
            },
            "postcode": {
                "postal_code": "int",
                "return": ""
            },
            "address": {
                "adr": "str",
                "return": ""
            }
        }
    }


# Calculates fire risk based on raw data supplied by the user.
@app.post("/fireguard/services/rawdata")
async def raw_data(temp: float, temp_forecast: float, humidity: float, humidity_forecast: float, wind_speed: float, wind_speed_forecast: float, timestamp: str, timestamp_forecast: str, long: float, lat: float):
    
    frc = FireRiskAPI(client=None) # IMPORTANT: the client is set to "None" as we do not require the use of a met client for the raw data functions. Never use fucntions that require this client with this instance.

    predictions = frc.compute_from_raw_data(temp=temp, temp_forecast=temp_forecast, humidity=humidity, humidity_forecast=humidity_forecast, wind_speed=wind_speed, wind_speed_forecast=wind_speed_forecast, timestamp=dateutil.parser.parse(timestamp), timestamp_forecast=dateutil.parser.parse(timestamp_forecast), long=long, lat=lat)

    return predictions


# Default for area selection. Returns expected input variables for the area service functions.
@app.get("/fireguard/services/area")
async def area():
    return {
        "message": "Område tjeneste frå FireGuard, brannrisiko basert på værdata frå lokasjonar.",
        "area": {
            "gps": {
                "lon": "float", 
                "lat": "float",
                "days (optional, default = 1, minimum = 1)": "int",
                "return": ""
            },
            "postcode": {
                "postal_code": "int",
                "return": ""
            },
            "address": {
                "adr": "str",
                "return": ""
            }
        }
    }


# Calculates fire risk based on GPS coordinates supplied by the user.
@app.get("/fireguard/services/area/gps")
async def gps (lon: float, lat: float, days: int = 1):
    """met_client = METClient()
    frc = FireRiskAPI(client=met_client)
    location = Location(longitude=lon, latitude=lat)
    obs_delta = datetime.timedelta(days=days)
    predictions = frc.compute_now(location=location, obs_delta=obs_delta)"""

    print("Accepted request for GPS")

    # Make a key and queue a request.
    with threading.Lock():
        key = logic_handler.handle_request("gps", [lon, lat])

        print("Sent request for GPS")
        print(logic_handler.results[key])

    result: list

    # Have the thread continuously check if the temporary storage has updated to contain a list of FireRiskPredictions. Once this is the case, return the results stored.
    #TODO: Change the result type to be a JSON formatted result for the end user.
    while True:
        time.sleep(1)
        with threading.Lock():
            print(f"Waiting for result . . . {logic_handler.results[key]}")
            if type(logic_handler.results[key]) == list:
                result = logic_handler.results[key]
                logic_handler.results.pop(key)
                break

    return result


# Calculates fire risk based on postcode. Uses separate API to determine coordinates for the post code.
@app.get("/fireguard/services/area/postcode")
async def postcode (postal_code: int):
    # TODO: [FIR-57] Implement RestAPI methods. Requires the use of Kartverket's geocoding api.
    pass


# Calculates fire risk based on address. Uses separate API to determine coordinates for the address.
@app.get("/fireguard/services/area/address")
async def address (adr: str):
    # TODO: [FIR-57] Implement RestAPI methods. Requires the use of Kartverket's geocoding api.
    pass