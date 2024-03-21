import threading
import time
import random

from frcm.datamodel.model import FireRiskPrediction
from frcm.weatherdata.positiondata.client_geocoding import GeoCodingClient
from frcm.weatherdata.client_met import WeatherDataClient

class LogicHandler():


    """
    THREAD PROTECTED VARIABLES

    active_threads
    waiting_list
    
    """

    def __init__(self) -> None:
        #self.handler_metclient = LogicHandlerMETClient()
        #self.handler_geoclient = LogicHandlerGEOClient()

        self.lock = threading.Lock()
        self.waiting_list = []
        self.max_threads = 6 # constant
        self.active_threads = 0
        print("LogicHandler started up")

        # Start looping through the waiting list and check every second if there is an open slot for a request to be handled.
        self.queue_manager = threading.Thread(target=self.start_waiting_requests)
        self.queue_manager.start()
        print("Queue manager started up")

        # dictionary for storing result values
        self.results: dict = {}


    def lookup_database (self):
        # TODO 
        return False


    def make_request (self, data: list) -> list[FireRiskPrediction]:
        """
            Determines first if data exists in Database already.
            If not, determines what type of request is being amde, e.g. gps coordinates, rawdata, address, etc.
            Sends the request to appriopriate subclass for coordinating with the Geo- and Met clients.
            Returns resulting calculation once the entire process is done.
        """

        randomized_key = data[0]
        req_type = data[1]
        request_data = data[2]

        if self.lookup_database:
            result = "shit" #TODO Ve so snill å husk å fjerna denne før me leverer <3
            self.lock.acquire()

            self.results[randomized_key] = result

            self.lock.release()
            return 

        result: list[FireRiskPrediction]

        if req_type == "gps":
            result = ["test gps"]
        elif req_type == "rawdata":
            result = ["test rawdata"]
        else:
            self.handler_geoclient.make_request(data=data)

        self.lock.acquire() # Lock protected objects

        self.active_threads -= 1
        self.results[randomized_key] = result

        self.lock.release() # Relase protected objects


    def process_request(self, data):
        """
            accepts
        """
        print(f"Request {data} with key processed by thread {threading.current_thread().name}")
        self.make_request(data=data)


    def handle_request(self, req_type, data):
        with self.lock:
            if self.active_threads < self.max_threads:
                
                self.lock.acquire() # Lock protected objects

                self.active_threads += 1

                # Create randomized key. Checks if randomized key exists already in the dictionary. In that case keep getting new randomized key and checking for duplicates and stops immediately when there is no longer a duplicate key in the dictionary.
                randomized_key = random.randint(0, 1000000000000)
                """while randomized_key in list(self.results.keys()):
                    print(randomized_key)
                    randomized_key = random.randint(0, 1000000000000)"""
                self.results[randomized_key] = "placeholder"
                print(randomized_key)

                self.lock.release() # Relase protected objects

                # Start a new thread
                thread = threading.Thread(target=self.process_request, args=([randomized_key, req_type, data],))
                thread.start()
                return randomized_key
                
            else:
                
                self.lock.acquire() # Lock protected objects

                randomized_key = random.randint(0, 1000000000000)
                """while randomized_key in list(self.results.keys()):
                    print(randomized_key)
                    randomized_key = random.randint(0, 1000000000000)"""
                self.results[randomized_key] = "placeholder"
                print(randomized_key)

                # Add to waiting list
                self.waiting_list.append([randomized_key, req_type, data])
                print(f"Request type:{req_type} data:{data} added to waiting list with key {randomized_key} XD")

                self.lock.release() # Relase protected objects
                return randomized_key


    def start_waiting_requests(self):
        """
            Locks the current thread.
            Checks if number of active threads is less than max threads + 1 allowed at a single time.
            Checks if there are requests on the waiting list. If so, starts a thread with the request. If not, breaks out of the while loop.
        """
        while True:
            #time.sleep(1)
            with self.lock:

                self.lock.acquire() # Lock protected objects

                if self.waiting_list and self.active_threads < (self.max_threads + 1):
                    request = self.waiting_list.pop(0)
                    self.active_threads += 1
                    thread = threading.Thread(target=self.process_request, args=(request,))
                    thread.start()
                    
                    print(f"Request {request} started from waiting list!")
                else:
                    continue

                self.lock.release() # Relase protected objects


class LogicHandlerGEOClient (LogicHandler):

    # TODO: FIR-76 Exclude inherited Thread handling from LogicHandlerGEOCoding class.

    def __init__(self) -> None:
        self.client = GeoCodingClient()

    def make_request(self, data: list):
        pass


class LogicHandlerMETClient (LogicHandler):
    def __init__(self):
        self.lock = threading.Lock()
        self.waiting_list = []
        self.max_threads = 6
        self.active_threads = 0