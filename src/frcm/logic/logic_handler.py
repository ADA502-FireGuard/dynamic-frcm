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
        self.max_threads = 3 # constant
        self.active_threads = 0

        # Start looping through the waiting list and check every second if there is an open slot for a request to be handled.
        self.queue_manager = threading.Thread(target=self.queue_handler, daemon=True) #TODO: Should this be marked as a background thread or should it keep the program running? For now it is set as background thread.
        self.queue_manager.start()

        # dictionary for storing result values
        self.results: dict = {}


    def lookup_database (self):
        # TODO 
        return False


    def finish_request (self, data: list):
        pass


    def process_request(self, data):
        """
            Accepts the input data for a request and processes it. Prints out a message indicating that it is being handled.
            Determines first if data exists in Database already.
            If not, determines what type of request is being amde, e.g. gps coordinates, rawdata, address, etc.
            Sends the request to appriopriate subclass for coordinating with the Geo- and Met clients.
            Returns resulting calculation once the entire process is done.
        """
        print(f"Request with key: {data[0]}, request type: '{data[1]}' is being processed by thread {threading.current_thread().name}")

        randomized_key = data[0]
        req_type = data[1]
        request_data = data[2]

        with self.lock:
            if self.lookup_database():
                result = "shit" #TODO Ve so snill å husk å fjerna denne før me leverer <3
                self.results[randomized_key] = result
                return 

        result: list[FireRiskPrediction]

        if req_type == "gps":
            result = ["test gps"]
        elif req_type == "":
            pass
        elif req_type == "rawdata":
            result = ["test rawdata"]
        else:
            #self.handler_geoclient.finish_request(data=data)
            result = ["test else"] # TODO: Replace

        time.sleep(5)

        print(f"Thread {threading.current_thread().name} Finished handling request with key {randomized_key}")

        with threading.Lock():
            self.active_threads -= 1
            self.results[randomized_key] = result


    def handle_request(self, req_type, data) -> int:
        """
            Takes in information on request type and data associated with it, determines how many requests are currently being handled, and either starts a new thread to handle the request or adds the request to the waiting list.
            Creates a randomized key used to access the results once the request has been handled.
            Returns the randomized key, and temporarily sets the results dictionary's value corresponding to the key to be "placeholder" to simplify the requesting thread's checking if the request has been handled and finished by determining the type of the result stored.
        """
        randomized_key: int

        with threading.Lock():
            # Create randomized key. Checks if randomized key exists already in the dictionary. In that case keep getting new randomized key and checking for duplicates and stops immediately when there is no longer a duplicate key in the dictionary.
            randomized_key = random.randint(0, 10000000)
            while randomized_key in list(self.results.keys()):
                randomized_key = random.randint(0, 10000000)
            self.results[randomized_key] = "placeholder"

            if self.active_threads < self.max_threads:
                self.active_threads += 1
                # Start a new thread
                thread = threading.Thread(target=self.process_request, args=([randomized_key, req_type, data],))
                thread.start()
                
            else:
                # Add to waiting list
                self.waiting_list.append([randomized_key, req_type, data])
                print(f"Request type: {req_type} data: {data} added to waiting list with key: {randomized_key}")

        return randomized_key


    def queue_handler(self):
        """
            Locks the current thread.
            Checks if number of active threads is less than max threads + 1 allowed at a single time.
            Checks if there are requests on the waiting list. If so, starts a thread with the request. If not, breaks out of the while loop.
        """
        while True:
            time.sleep(1)
            with self.lock:
                print(f"Thread Queue Handler loop running . . . Active Threads: {self.active_threads} . . . Queued Threads: {len(self.waiting_list)}")
                if self.waiting_list and self.active_threads < (self.max_threads + 1):
                    request = self.waiting_list.pop(0)
                    self.active_threads += 1
                    thread = threading.Thread(target=self.process_request, args=(request,))
                    thread.start()
                    
                    print(f"Request {request} started from waiting list!")
                else:
                    continue



class LogicHandlerGEOClient (LogicHandler):

    # TODO: FIR-76 Exclude inherited Thread handling from LogicHandlerGEOCoding class.

    def __init__(self) -> None:
        self.client = GeoCodingClient()

    def finish_request(self, data: list):
        pass


class LogicHandlerMETClient (LogicHandler):
    def __init__(self):
        self.waiting_list = []
        self.max_threads = 6
        self.active_threads = 0