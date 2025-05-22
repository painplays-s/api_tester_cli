import unittest
from ..api_client.http_client import HttpClient
from unittest.mock import patch
import requests

class TestHttpClient(unittest.TestCase):
    def setUp(self):
        self.client = HttpClient()
        self.base_url = "https://jsonplaceholder.typicode.com"
        
    def test_get_request(self):
        response = self.client.get(f"{self.base_url}/posts/1")
        self.assertEqual(response['status_code'], 200)
        self.assertIn('title', response['body'])

    def test_post_request(self):
        test_data = {
            "title": "foo",
            "body": "bar",
            "userId": 1
        }
        response = self.client.post(f"{self.base_url}/posts", data=test_data)
        self.assertEqual(response['status_code'], 201)
        self.assertEqual(response['body']['title'], "foo")

    def test_put_request(self):
        test_data = {
            "id": 1,
            "title": "foo",
            "body": "bar",
            "userId": 1
        }
        response = self.client.put(f"{self.base_url}/posts/1", data=test_data)
        self.assertEqual(response['status_code'], 200)
        self.assertEqual(response['body']['title'], "foo")

    def test_delete_request(self):
        response = self.client.delete(f"{self.base_url}/posts/1")
        self.assertEqual(response['status_code'], 200)

    @patch('requests.get')
    def test_invalid_url(self, mock_get):
        # Mock the requests.get to raise ConnectionError
        mock_get.side_effect = requests.ConnectionError()
        
        with self.assertRaises(requests.ConnectionError):
            self.client.get("https://invalid-url")

    def test_set_headers(self):
        test_headers = {"Authorization": "Bearer token123"}
        self.client.set_headers(test_headers)
        self.assertEqual(self.client.headers["Authorization"], "Bearer token123")

if __name__ == '__main__':
    unittest.main()