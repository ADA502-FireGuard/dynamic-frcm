from fastapi import FastAPI, Response, status

from frcm.logic.logic_handler import LogicHandler
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
    #TODO 
    pass


# Default for services selection. Returns JSON containing info on available services, input variables required and return values.
@app.get("/fireguard/services")
async def services ():
    #TODO UPDATE THESE PATHS AND RETURN TYPES TO THE UPDATED ONES.
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
async def raw_data(temp: float, temp_forecast: float, humidity: float, humidity_forecast: float, wind_speed: float, wind_speed_forecast: float, timestamp: str, timestamp_forecast: str, lon: float, lat: float):
    print("Accepted request for raw data")

    data: dict = {
        "temp": temp,
        "temp_forecast": temp_forecast, 
        "humidity": humidity,
        "humidity_forecast": humidity_forecast,
        "wind_speed": wind_speed,
        "wind_speed_forecast": wind_speed_forecast,
        "timestamp": timestamp,
        "timestamp_forecast": timestamp_forecast,
        "lon": lon,
        "lat": lat
    }
    result: list

    # Make a key and queue a request.
    with threading.Lock():
        key = logic_handler.handle_request(req_type="rawdata", data=data)

        print("Sent request for raw data")

    # Have the thread continuously check if the temporary storage has updated to contain a list of FireRiskPredictions. Once this is the case, return the results stored.
    while True:
        time.sleep(1)
        with threading.Lock():
            print(f"Waiting for result . . . {key}")
            if type(logic_handler.results[key]) == list:
                result = logic_handler.results[key]
                logic_handler.results.pop(key)
                break

    return result


# Default for area selection. Returns expected input variables for the area service functions.
@app.get("/fireguard/services/area")
async def area():
    #TODO UPDATE THESE PATHS TO THE CORRECT VERSIONS
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
async def gps (lon: float, lat: float, days: float = 1.0):
    print("Accepted request for GPS")

    data: dict = {
        "lon": lon,
        "lat": lat, 
        "days": days
    }
    result: list

    # Make a key and queue a request.
    with threading.Lock():
        key = logic_handler.handle_request(req_type="gps", data=data)

        print("Sent request for GPS")

    # Have the thread continuously check if the temporary storage has updated to contain a list of FireRiskPredictions. Once this is the case, return the results stored.
    while True:
        time.sleep(1)
        with threading.Lock():
            print(f"Waiting for result . . . {key}")
            if type(logic_handler.results[key]) == list:
                result = logic_handler.results[key]
                logic_handler.results.pop(key)
                break

    return result


# Calculates fire risk based on multiple GPS coordinates supplied by the user.
@app.get("/fireguard/services/area/multiple_gps")
async def multiple_gps(lon: list[float], lat: list[float], days: list[float]):
    print("Accepted request for multiple GPS")
    if not len(lon) == len(lat) or not len(lon) == len(days) or not len(lat) == len(days):
        return "Error: size of lon, lat and/or days do not match."

    data: dict = {}
    result: list

    # Pack the data from the lists into the data dictionary for the request.
    for i in range(0, len(lon)):
        data_point: dict = {
            "lon": lon[i],
            "lat": lat[i],
            "days": days[i]
        }
        data[i] = data_point

    # Make a key and queue a request.
    with threading.Lock():
        key = logic_handler.handle_request(req_type="multiple_gps", data=data)

        print("Sent request for multiple GPS")

    # Have the thread continuously check if the temporary storage has updated to contain a list of FireRiskPredictions. Once this is the case, return the results stored.
    while True:
        time.sleep(1)
        with threading.Lock():
            print(f"Waiting for result . . . {key}")
            if type(logic_handler.results[key]) == list:
                result = logic_handler.results[key]
                logic_handler.results.pop(key)
                break

    return result


# Calculates fire risk based on postcode. Uses separate API to determine coordinates for the post code.
@app.get("/fireguard/services/area/postcode")
async def postcode (postal_code: int, days: float):
    print("Accepted request for postal code")

    data: dict = {
        "postal_code": postal_code,
        "days": days
    }
    result: list

    # Make a key and queue a request.
    with threading.Lock():
        key = logic_handler.handle_request(req_type="postal_code", data=data)

        print("Sent request for postal code")

    # Have the thread continuously check if the temporary storage has updated to contain a list of FireRiskPredictions. Once this is the case, return the results stored.
    while True:
        time.sleep(1)
        with threading.Lock():
            print(f"Waiting for result . . . {key}")
            if type(logic_handler.results[key]) == list:
                result = logic_handler.results[key]
                logic_handler.results.pop(key)
                break

    return result


# Calculates fire risk based on address. Uses separate API to determine coordinates for the address.
@app.get("/fireguard/services/area/address")
async def address (adr: str, days: float):
    print("Accepted request for address")

    data: dict = {
        "address": adr,
        "days": days
    }
    result: list

    # Make a key and queue a request.
    with threading.Lock():
        key = logic_handler.handle_request(req_type="address", data=data)

        print("Sent request for address")

    # Have the thread continuously check if the temporary storage has updated to contain a list of FireRiskPredictions. Once this is the case, return the results stored.
    while True:
        time.sleep(1)
        with threading.Lock():
            print(f"Waiting for result . . . {key}")
            if type(logic_handler.results[key]) == list:
                result = logic_handler.results[key]
                logic_handler.results.pop(key)
                break

    return result
