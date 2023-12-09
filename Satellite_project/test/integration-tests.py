import unittest
import requests

class TestIntegration(unittest.TestCase):

    def testDataCollectionPipeline(self):
        
        frontendPost = {"latitude": 74.32, "longitude": 120.23}
        backend_response = requests.post('http://127.0.0.1:5001/send-coordinates', json=frontendPost)
        response_data = backend_response.json()

        self.assertEqual(backend_response.status_code, 200)
        self.assertEqual(type(response_data), list)

        ## this endpoint queries an external api, meaning that there is a possibility there is no satellites in the vicinity making it empty
        if response_data:
            self.assertEqual(type(response_data[0]), dict)
            self.assertTrue(all(['satid' in satellite for satellite in response_data]))
            self.assertTrue(all(['satname' in satellite for satellite in response_data]))
            self.assertTrue(all(['satlatitude' in satellite for satellite in response_data]))
            self.assertTrue(all(['satlongitude' in satellite for satellite in response_data]))
            self.assertTrue(all(['sataltitude' in satellite for satellite in response_data]))


    def testOrbitsPipeline(self):

        FrontendPost = {'type': 'orbits'}
        response = requests.post('http://127.0.0.1:5001/send-to-analyzer', json=FrontendPost)
        response_data = response.json()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(type(response_data), dict)
        self.assertTrue('LEO'in response_data['labels'])
        self.assertTrue('MEO'in response_data['labels'])
        self.assertEqual(type(response_data['datasets'][0]), dict)
        self.assertEqual(type(response_data['datasets'][0]['data']), list)


    def testMapPipeline(self):

        FrontendPost = {'satname': 'HELLOWORLD', 'satlatitude': '0', 'satlongitude': '0', 'sataltitude': '0', 'includes': "all", 'type': "map"}
        response = requests.post('http://127.0.0.1:5001/send-to-analyzer', json=FrontendPost)
        response_data = response.json()

       
        self.assertEqual(response.status_code, 200)
        self.assertEqual(type(response_data), list)

        ## this endpoint queries the database. If there is no data, this will be empty
        ## This returns the same thing as the collector, it only essentially filters
        if response_data:
            self.assertEqual(type(response_data[0]), dict)
            self.assertTrue(all(['satid' in satellite for satellite in response_data]))
            self.assertTrue(all(['satname' in satellite for satellite in response_data]))
            self.assertTrue(all(['satlatitude' in satellite for satellite in response_data]))
            self.assertTrue(all(['satlongitude' in satellite for satellite in response_data]))
            self.assertTrue(all(['sataltitude' in satellite for satellite in response_data]))


if __name__ == '__main__':
    unittest.main()