import unittest
from unittest.mock import patch  
from Components.WebApplication.src.Backend.app import create_app

class TestBackend(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    @patch('requests.get')
    @patch('requests.post')
    def testSendCoordinates(self, mock_post, mock_get):
        #mock is part of /send-coordinates endpoint, it is mocking a successful get-satellites endpoint response
        mock_post.return_value.status_code = 201
        mock_post.return_value.json.return_value = "Successfully committed satellites"

        #mock_Get is part of /Observeable-satellites endpoint
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = [{'satid': '24',
                                'satname':'BIGSATELLITE',
                                'satlatitude':'120',
                                'satlongitude':'-15.23',
                                'sataltitude':'4000'},
                                {'satid': '24324',
                                'satname':'NOTBIGSATELLITE',
                                'satlatitude':'120',
                                'satlongitude':'-15.23',
                                'sataltitude':'4000'}]
        
        frontendPost = {"latitude": 74.32, "longitude": 120.23}
        response = self.client.post('http://127.0.0.1:5001/send-coordinates', json=frontendPost)
        self.assertEqual(response.status_code, 200)

        mock_post.assert_called_once()
        call = mock_post.call_args

        self.assertEqual(call[0][0], 'http://127.0.0.1:5003/get-satellites') 
        self.assertEqual(call[1]['json'], {'latitude':74.32, 'longitude':120.23})

        mock_get.assert_called_once_with('http://127.0.0.1:5001/Observable-satellites?latitude=74.32&longitude=120.23')



    @patch('Components.schemas_queries.getSatellites')
    def testObservableSatellites(self, mock_db):
        mock_db.return_value = [{'satid': '24',
                                'satname':'BIGSATELLITE',
                                'satlatitude':'120',
                                'satlongitude':'-15.23',
                                'sataltitude':'4000'},
                                {'satid': '24324',
                                'satname':'NOTBIGSATELLITE',
                                'satlatitude':'120',
                                'satlongitude':'-15.23',
                                'sataltitude':'4000'}]

        # Test out params and response for a few cases to test functionality
        params = {"latitude": 0, "longitude": 0}
        response = self.client.get('http://127.0.0.1:5001/Observable-satellites', query_string=params)
        self.assertEqual(response.status_code, 200)

        mock_db.assert_called_with(latitude=0, longitude=0)

        params = {"latitude": -50.23, "longitude": 125.32}
        response = self.client.get('http://127.0.0.1:5001/Observable-satellites', query_string=params)
        self.assertEqual(response.status_code, 200)

        mock_db.assert_called_with(latitude=-50.23, longitude=125.32)

        response_data = response.get_json()
        self.assertEqual(response_data[0]['satname'], 'BIGSATELLITE')
        self.assertEqual(response_data[1]['satname'], 'NOTBIGSATELLITE')
        self.assertEqual(response_data[0]['satid'], '24')
        self.assertEqual(response_data[1]['satid'], '24324')


    @patch('requests.post')
    def testSendDataAnalyzer(self, mock_analyzer):
        #Mocking a successful orbit-calculations endpoint response
        mock_analyzer.return_value.status_code = 200  
        mock_analyzer.return_value.json.return_value = {
            'labels':["LEO","MEO","HEO","GEO"],
            'datasets' : [{
                'label': "Satellites in orbit categories",
                'data': [124, 560, 3000, 3]            
            }]
        }

        data = {"type": "orbits"}
        response = self.client.post('http://127.0.0.1:5001/send-to-analyzer', json=data)
        self.assertEqual(response.status_code, 200)

        mock_analyzer.assert_called_once()
        call = mock_analyzer.call_args

        self.assertEqual(call[0][0], 'http://127.0.0.1:5002/orbit-calculations') 
        self.assertEqual(call[1]['json'], {"type": "orbits"})


if __name__ == '__main__':
    unittest.main()