from fastapi import FastAPI
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

    met_extractor = METExtractor()

    # TODO: maybe embed extractor into client
    met_client = METClient(extractor=met_extractor)

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

app = FastAPI()

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
            "humidity": "float",
            "wind_speed": "float",
            "timestamp": "str",
            "return": ""
        },
        "area": {
            "gps": {
                "lon": "float", 
                "lat": "float",
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
@app.get("/fireguard/services/rawdata")
async def raw_data(temp: float, humidity: float, wind_speed: float, timestamp: str):
    
    timestamp = dateutil.parser.parse(timestamp)
    wd_point = WeatherDataPoint(temperature=temp,
                                    humidity=humidity,
                                    wind_speed=wind_speed,
                                    timestamp=timestamp)
    data:list
    data.append(wd_point)
    print(data)

    met_extractor = METExtractor()

    met_client = METClient(extractor=met_extractor)

    frcapi = FireRiskAPI(client=met_client)

    location_dummy = Location(latitude=0.0, longitude=0.0)

    obs_delta = datetime.timedelta(seconds=1)

    predictions = frcapi.compute_now(location=location_dummy, obs_delta=obs_delta)

    print(predictions)


# Default for area selection. Returns expected input variables for the area service functions.
@app.get("/fireguard/services/area")
async def area():
    return {
        "message": "Område tjeneste frå FireGuard, brannrisiko basert på værdata frå lokasjonar.",
        "area": {
            "gps": {
                "lon": "float", 
                "lat": "float",
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
async def gps (lon: float, lat: float):
    pass


# Calculates fire risk based on postcode. Uses separate API to determine coordinates for the post code.
@app.get("/fireguard/services/area/postcode")
async def postcode (postal_code: int):
    pass


# Calculates fire risk based on address. Uses separate API to determine coordinates for the address.
@app.get("/fireguard/services/area/address")
async def address (adr: str):
    pass