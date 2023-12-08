import unittest
from unittest.mock import patch  
from DataAnalyzer.src.data_analyzer import create_app as create_app_analyzer
from DataCollector.src.data_collector import create_app as create_app_collector
from WebApplication.Backend.app import create_app as create_app_backend
from WebApplication.Frontend.front_app import create_app as create_app_frontend

class TestDatabase(unittest.TestCase):
    def setUp(self):
        self.analyzer = create_app_analyzer()
        self.collector = create_app_collector()
        self.backend = create_app_backend()
        self.frontend = create_app_frontend()


    def testDataCollectionPipeline(self):
        pass


    def testDataAnalyzingPipeline(self):
        pass


if __name__ == '__main__':
    unittest.main()