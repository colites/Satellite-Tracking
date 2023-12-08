import unittest
from unittest.mock import patch  
from DataCollector.src.data_collector import create_app

class TestBackend(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    @patch('pika.BlockingConnection')
    @patch('requests.get')
    def testGetSatellitesAPI(self, mock_get, mock_queue_connection):
        #mock is part of /send-coordinates endpoint
        mock_get.return_value.status_code = 200  
        mock_get.return_value.json.return_value = {
                                                    "info": {
                                                        "category": "Amateur radio",
                                                        "transactionscount": 1,
                                                        "satcount": 1
                                                    },
                                                    "above": [
                                                        {
                                                        "satid": 2042,
                                                        "satname": "HELLO",
                                                        "intDesignator": "1990-013C",
                                                        "launchDate": "1990-02-07",
                                                        "satlat": 25.34,
                                                        "satlng": -92.5032,
                                                        "satalt": 124.923
                                                        }
                                                    ]}
        
        mock_channel = mock_queue_connection.return_value.channel.return_value
        mock_channel.queue_declare.return_value = None
        mock_channel.basic_publish.return_value = None

        data = {"latitude" : 74.32, "longitude" : 120.23}
        response = self.client.post('http://127.0.0.1:5003/get-satellites', json=data)
        self.assertEqual(response.status_code, 201)
        
        # Check for the right arguments in the API call
        mock_get.assert_called_once_with('https://api.n2yo.com/rest/v1/satellite/above/74.32/120.23/0/30/0/&apiKey=777RKY-662TWA-KAK8Z7-55Y1')
        mock_channel.basic_publish.assert_called_once_with(exchange='', 
                                                           routing_key='database_queue', 
                                                           body=b'{"data": {"info": {"category": "Amateur radio", "transactionscount": 1, "satcount": 1}, "above": [{"satid": 2042, "satname": "HELLO", "intDesignator": "1990-013C", "launchDate": "1990-02-07", "satlat": 25.34, "satlng": -92.5032, "satalt": 124.923}]}, "latitude": 74.32, "longitude": 120.23}')



if __name__ == '__main__':
    unittest.main()