import threading
import time
import datetime
import psycopg2
from psycopg2 import sql

from frcm.datamodel.model import FireRiskPrediction, Location

class DatabaseHandler:

    def __init__(self, database_url):
        self.database_url = database_url
        self.conn = None
        self.open_database()


    def open_database(self):
        """
            Opens the database.
        """
        try:
            self.conn = psycopg2.connect(self.database_url)
            print("Database connection opened successfully.")
        except Exception as e:
            print(f"An error occurred while connecting to the database: {e}")


    def close_database(self):
        """
            Closes the database.
        """
        if self.conn:
            self.conn.close()
            print("Database connection closed.")
            

    def append_database_item(self, firerisk, lon, lat, source):
        """
            Adds an item to the database.
        """
        try:
            with self.conn.cursor() as cur:
                query = sql.SQL("""
                    INSERT INTO FireRiskData (FireRisk, Lon, Lat, Source)
                    VALUES (%s, %s, %s, %s)
                """)
                cur.execute(
                    query,
                    [str(firerisk), str(lon), str(lat), source]  # Pass the parameters as a list, not part of the SQL object
                )
                self.conn.commit()
                print("FireRiskData item appended to database.")
        except Exception as e:
            self.conn.rollback()
            print(f"An error occurred while appending to the database: {e}")


    def init_check_database (self):
        """
            Makes initial checks on the database during startup of the program.
        """
        #TODO Database handler
        pass


    def database_timer (self):
        """
            Runs a timer that checks the items inside the database for expiration and starts the removal- or renewal processes. 
            Also handles checking subscriptions and starts renewal of data- and sending of data processes.
        """
        #TODO Database handler
        while True:
            time.sleep(60)

            with self.lock:
                pass


    def update_database_item (self):
        """
            Updates an item in the database by making a request to the Logic Handler for processing new data.
        """
        #TODO Database handler
        pass


    def remove_database_item (self):
        """
            Removes an item from the database.
        """
        #TODO Database handler
        pass


