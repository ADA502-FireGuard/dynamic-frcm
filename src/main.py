from fastapi import FastAPI, Response, status
from fastapi import FastAPI, Response, status
from frcm.weatherdata.utils import weatherdata_parse
from frcm.datamodel.model import WeatherDataPoint
from frcm.frcapi import FireRiskAPI
from frcm.weatherdata.client_met import METClient
from frcm.weatherdata.extractor_met import METExtractor
from frcm.datamodel.model import Location
import datetime
import dateutil.parser

# sample code illustrating how to use the Fire Risk Computation API (FRCAPI)
if __name__ == "__main__":

    met_client = METClient()
    met_client = METClient()

    frc = FireRiskAPI(client=met_client)

    location = Location(latitude=60.383, longitude=5.3327)  # Bergen
    # location = Location(latitude=59.4225, longitude=5.2480)  # Haugesund

    # Fails
    # location = Location(latitude=62.5780, longitude=11.3919)  # Røros
    # location = Location(latitude=69.6492, longitude=18.9553)  # Tromsø

    # how far into the past to fetch observations

    obs_delta = datetime.timedelta(days=2)

    #predictions = frc.compute_now(location, obs_delta)

    #print(predictions)


# Start of RestAPI implementation. Below is defined all the paths that are used to access the FireGuard Cloud Service.

# Start of RestAPI implementation. Below is defined all the paths that are used to access the FireGuard Cloud Service.
app = FastAPI()

# Root. Returns a simple message to confirm that the user can reach the FireGuard Cloud Service.
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
                "days": "int",
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

    predictions = frc.compute_from_raw_data(temp=temp, temp_forecast=temp_forecast, humidity=humidity, humidity_forecast=humidity_forecast, wind_speed=wind_speed, wind_speed_forecast=wind_speed_forecast, timestamp=timestamp, timestamp_forecast=timestamp_forecast, long=long, lat=lat)

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
                "days (optional)": "int",
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
async def gps (lon: float, lat: float, days: int = 0):
    met_client = METClient()
    frc = FireRiskAPI(client=met_client)
    location = Location(longitude=lon, latitude=lat)
    obs_delta = datetime.timedelta(days=days)
    predictions = frc.compute_now(location=location, obs_delta=obs_delta)
    return predictions


# Calculates fire risk based on postcode. Uses separate API to determine coordinates for the post code.
@app.get("/fireguard/services/area/postcode")
async def postcode (postal_code: int):
    pass


# Calculates fire risk based on address. Uses separate API to determine coordinates for the address.
@app.get("/fireguard/services/area/address")
async def address (adr: str):
    pass