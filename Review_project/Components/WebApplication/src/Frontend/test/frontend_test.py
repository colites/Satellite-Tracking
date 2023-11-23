import unittest
from unittest.mock import patch  
from datetime import date
from ..front_app import create_app


class TestFrontend(unittest.TestCase):

    def setUP(self):
        self.app = create_app(testing=True)
        self.client = self.app.test_client()


    def frontendRoutes(self):
        pass


if __name__ == '__main__':
    unittest.main()