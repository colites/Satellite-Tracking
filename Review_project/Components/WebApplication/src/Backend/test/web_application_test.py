import unittest
from unittest.mock import patch  
from datetime import date
from Backend.app import create_app

class TestBackend(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()


    def testSubmitReview(self):
        pass


    @patch('Backend.schemas_queries.getProductReviewsQuery')
    def testSendDataFrontend(self, getProductReviewsQuery):

        getProductReviewsQuery.return_value = {'reviews': [(date.today(), "orange", "very good product", 5), 
                                                           (date.today(), "orange", "this orange was decent but seen better", 3)]}
        
        ## valid value with actual query results
        response = self.client.get('http://127.0.0.1:5001/query-data-frontend?productName=orange')
        self.assertEqual(response.status_code, 200)
        getProductReviewsQuery.assert_called_once_with("orange")
        self.assertEqual(2, len(response.get_json()['reviews']))

        #invalid empty value
        response = self.client.get('http://127.0.0.1:5001/query-data-frontend?productName=')
        self.assertEqual(response.status_code, 400)

        #valid productName with no query results
        getProductReviewsQuery.return_value = {'reviews': []}
        response = self.client.get('http://127.0.0.1:5001/query-data-frontend?productName=asdgsdagweg')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {'reviews': []})
        self.assertEqual(0, len(response.get_json()['reviews']))


if __name__ == '__main__':
    unittest.main()