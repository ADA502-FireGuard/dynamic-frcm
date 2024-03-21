import unittest

from frcm.logic.logic_handler import LogicHandler
from frcm.datamodel.model import FireRiskPrediction

class TestLogicHandler (unittest.TestCase):
    def setUp(self) -> None:
        self.logic_handler = LogicHandler()

    
    def test_handle_request (self):

        key1 = self.logic_handler.handle_request("test", ["data1", "data2"])
        key2 = self.logic_handler.handle_request("test", ["data1", "data2"])

        self.assertTrue((not key1 == key2))
        self.assertTrue(type(key1) == int)

        #expected_firerisk_key1 = [FireRiskPrediction()]

        self.assertEqual(self.logic_handler.results[key1], )

        #TODO: Finish tests after API functions are properly implemented into handle_request


    def test_process_request (self):
        pass


    def test_finish_request (self):
        pass


    def test_lookup_database (self):
        pass 