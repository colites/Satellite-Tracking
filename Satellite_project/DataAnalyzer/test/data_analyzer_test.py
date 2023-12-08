import unittest
from unittest.mock import patch  
from DataAnalyzer.src.data_analyzer import create_app

class TestBackend(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    @patch('schemas_queries.getSatellitesFiltered')
    @patch('schemas_queries.getAllSatellites')
    def testMakeMap(self, mock_db, mock_db_filtered):
        mock_db.return_value = [{'satid': '11', 'satname':'ALIENS', 'satlatitude':'-0.52', 'satlongitude':'100.23', 'sataltitude':'4000'},
                                {'satid': '24422', 'satname':'NOTBIGSATELLITE', 'satlatitude':'0', 'satlongitude':'0', 'sataltitude':'40'}
                                ]
        mock_db_filtered.return_value = [{'satid': '24422', 'satname':'HELLOWORLD', 'satlatitude':'0', 'satlongitude':'0', 'sataltitude':'0'}]
        
        #enters the first mock_db, where it just returns all the satellites
        data = {'satname': 'HELLOWORLD', 'satlatitude': '0', 'satlongitude': '0', 'sataltitude': '0', 'includes': "all", 'type': "map"}
        response = self.client.post('http://127.0.0.1:5002/make-map', json=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(),[{'satid': '11', 'satname':'ALIENS', 'satlatitude':'-0.52', 'satlongitude':'100.23', 'sataltitude':'4000'},
                                {'satid': '24422', 'satname':'NOTBIGSATELLITE', 'satlatitude':'0', 'satlongitude':'0', 'sataltitude':'40'}
                                ])
        
        #enters the second mock_db, where it returns the filtered satellites based on frontend filters
        data = {'satname': 'HELLOWORLD', 'satlatitude': '0', 'satlongitude': '0', 'sataltitude': '0', 'includes': "filtered", 'type': "map"}
        response = self.client.post('http://127.0.0.1:5002/make-map', json=data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(),[{'satid': '24422', 'satname':'HELLOWORLD', 'satlatitude':'0', 'satlongitude':'0', 'sataltitude':'0'}])

    @patch('schemas_queries.getAllSatellites')
    def testOrbitCalculations(self, mock_db):
        mock_db.return_value = [{'satid': '11', 'satname':'ALIENS', 'satlatitude':'-0.52', 'satlongitude':'100.23', 'sataltitude':'4000'},
                                {'satid': '24422', 'satname':'NOTBIGSATELLITE', 'satlatitude':'0', 'satlongitude':'0', 'sataltitude':'40'}
                                ]
        
        response = self.client.get('http://127.0.0.1:5002/orbit-calculations')
        self.assertEqual(response.status_code, 200)

        ## first go into datasets, since its a list technically, go into first index, which is 0, and then to data field in that dictionary, which gives the sizes of the orbits.

        ## One below 2000 km and one above 2000 but below 35785
        self.assertEqual(response.get_json()['datasets'][0]['data'], [1,1,0,0])

        mock_db.return_value = [{'satid': '11', 'satname':'ALIENS', 'satlatitude':'-0.52', 'satlongitude':'100.23', 'sataltitude':'4000'},
                                {'satid': '24422', 'satname':'NOTBIGSATELLITE', 'satlatitude':'0', 'satlongitude':'0', 'sataltitude':'2000'}
                                ]
        
        response = self.client.get('http://127.0.0.1:5002/orbit-calculations')
        ## One at exactly 2000 km and one above 2000 but below 35785
        self.assertEqual(response.get_json()['datasets'][0]['data'], [1,1,0,0])

        mock_db.return_value = [{'satid': '11', 'satname':'ALIENS', 'satlatitude':'-0.52', 'satlongitude':'100.23', 'sataltitude':'4000'},
                                {'satid': '24422', 'satname':'NOTBIGSATELLITE', 'satlatitude':'0', 'satlongitude':'0', 'sataltitude':'2000'},
                                {'satid': '24422', 'satname':'NOTBIGSATELLITE', 'satlatitude':'0', 'satlongitude':'0', 'sataltitude':'40000'}, 
                                {'satid': '24422', 'satname':'NOTBIGSATELLITE', 'satlatitude':'0', 'satlongitude':'0', 'sataltitude':'35785'},
                                {'satid': '24422', 'satname':'NOTBIGSATELLITE', 'satlatitude':'0', 'satlongitude':'0', 'sataltitude':'35787'}  
                                ]
        
        response = self.client.get('http://127.0.0.1:5002/orbit-calculations')
        self.assertEqual(response.get_json()['datasets'][0]['data'], [1,1,1,2])


if __name__ == '__main__':
    unittest.main()