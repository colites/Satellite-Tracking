import unittest
from unittest.mock import patch  
from WebApplication.Backend.app import create_app

class TestBackend(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
    
    @patch('requests.get')
    @patch('requests.post')
    def testSendCoordinates(self, mock_post, mock_get):

        #the mock_push method simulates prometheus pushing to gateway server on tests so it is empty

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
        response = self.client.post('https://backend-q6r6.onrender.com/send-coordinates', json=frontendPost)
        self.assertEqual(response.status_code, 200)

        mock_post.assert_called_once()
        call = mock_post.call_args

        self.assertEqual(call[0][0], 'https://data-collector-r7r1.onrender.com/get-satellites') 
        self.assertEqual(call[1]['json'], {'latitude':74.32, 'longitude':120.23})

        mock_get.assert_called_once_with('https://backend-q6r6.onrender.com/Observable-satellites?latitude=74.32&longitude=120.23')



    @patch('schemas_queries.getSatellites')
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
        response = self.client.get('https://backend-q6r6.onrender.com/Observable-satellites', query_string=params)
        self.assertEqual(response.status_code, 200)

        mock_db.assert_called_with(latitude=0, longitude=0)

        params = {"latitude": -50.23, "longitude": 125.32}
        response = self.client.get('https://backend-q6r6.onrender.com/Observable-satellites', query_string=params)
        self.assertEqual(response.status_code, 200)

        mock_db.assert_called_with(latitude=-50.23, longitude=125.32)

        response_data = response.get_json()
        self.assertEqual(response_data[0]['satname'], 'BIGSATELLITE')
        self.assertEqual(response_data[1]['satname'], 'NOTBIGSATELLITE')
        self.assertEqual(response_data[0]['satid'], '24')
        self.assertEqual(response_data[1]['satid'], '24324')

    @patch('requests.get')
    @patch('requests.post')
    def testSendDataAnalyzer(self, mock_post, mock_analyzer_get):
        #Mocking a successful orbit-calculations endpoint response
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = [{'satid': '24',
                                'satname':'BIGSATELLITE',
                                'satlatitude':'120',
                                'satlongitude':'-15.23',
                                'sataltitude':'4000'},
                                {'satid': '24324',
                                'satname':'NOTBIGSATELLITE',
                                'satlatitude':'120',
                                'satlongitude':'-15.23',
                                'sataltitude':'4000'}]
        
        mock_analyzer_get.return_value.status_code = 200  
        mock_analyzer_get.return_value.json.return_value = {
            'labels':["LEO","MEO","HEO","GEO"],
            'datasets' : [{
                'label': "Satellites in orbit categories",
                'data': [124, 560, 3000, 3]            
            }]
        }

        ## when choosing the orbits endpoint
        data = {"type": "orbits"}
        response = self.client.post('https://backend-q6r6.onrender.com/send-to-analyzer', json=data)
        self.assertEqual(response.status_code, 200)

        mock_analyzer_get.assert_called_once()
        call = mock_analyzer_get.call_args

        self.assertEqual(call[0][0], 'https://data-analyzer.onrender.com/orbit-calculations') 
        self.assertEqual(call[1], {})

        ## when choosing the maps endpoint
        data = {'satname': 'HELLOWORLD', 'satlatitude': '0', 'satlongitude': '0', 'sataltitude': '0', 'includes': "all", 'type': "map"}
        response = self.client.post('https://backend-q6r6.onrender.com/send-to-analyzer', json=data)
        self.assertEqual(response.status_code, 200)

        mock_post.assert_called_once()
        call = mock_post.call_args

        self.assertEqual(call[0][0], 'https://data-analyzer.onrender.com/make-map') 
        self.assertEqual(call[1]['json'], {'satname': 'HELLOWORLD', 'satlatitude': '0', 'satlongitude': '0', 'sataltitude': '0', 'includes': "all", 'type': "map"})


if __name__ == '__main__':
    unittest.main()