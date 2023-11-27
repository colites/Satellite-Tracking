import unittest
from unittest.mock import patch  
from datetime import date
from WebApplication.src.Backend.app import create_app

class TestBackend(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    @patch('requests.post')
    def testSendCoordinates(self, mock):
        #mock is part of /send-coordinates endpoint
        mock.return_value.status_code = 200  
        mock.return_value.json.return_value = "Successfully committed satellites"

        frontendPost = {"latitude" : 74.32, "longitude" : 120.23}
        response = self.client.post('http://127.0.0.1:5001/send-coordinates', json=frontendPost)
        self.assertEqual(response.status_code, 200)

        
        mock.assert_called_once()
        call = mock.call_args

        self.assertEqual(call[0][0], 'http://127.0.0.1:5003/get-satellites') 
        self.assertEqual(call[1]['json'], (74.32, 120.23))


if __name__ == '__main__':
    unittest.main()