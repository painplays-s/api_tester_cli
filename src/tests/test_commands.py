import unittest
from unittest.mock import Mock, patch
from ..commands.get_command import execute_get_request
from ..commands.post_command import execute_post_request
from ..commands.put_command import execute_put_request
from ..commands.delete_command import execute_delete_request

class TestCommands(unittest.TestCase):
    def setUp(self):
        self.test_url = "http://api.test.com/endpoint"
        self.test_data = {"key": "value"}
        self.mock_response = {
            "status_code": 200,
            "headers": {"Content-Type": "application/json"},
            "body": {"result": "success"},
            "elapsed_time": 0.1
        }

    @patch('commands.get_command.HttpClient')
    def test_execute_get_request(self, mock_client):
        # Setup mock
        instance = mock_client.return_value
        instance.get.return_value = self.mock_response

        # Execute
        result = execute_get_request(self.test_url, params={"param": "value"})

        # Assert
        self.assertEqual(result, self.mock_response)
        instance.get.assert_called_once_with(self.test_url, params={"param": "value"})

    @patch('commands.post_command.HttpClient')
    def test_execute_post_request(self, mock_client):
        # Setup mock
        instance = mock_client.return_value
        instance.post.return_value = self.mock_response

        # Execute
        result = execute_post_request(self.test_url, data=self.test_data)

        # Assert
        self.assertEqual(result, self.mock_response)
        instance.post.assert_called_once_with(self.test_url, data=self.test_data)

    @patch('commands.put_command.HttpClient')
    def test_execute_put_request(self, mock_client):
        # Setup mock
        instance = mock_client.return_value
        instance.put.return_value = self.mock_response

        # Execute
        result = execute_put_request(self.test_url, data=self.test_data)

        # Assert
        self.assertEqual(result, self.mock_response)
        instance.put.assert_called_once_with(self.test_url, data=self.test_data)

    @patch('commands.delete_command.HttpClient')
    def test_execute_delete_request(self, mock_client):
        # Setup mock
        instance = mock_client.return_value
        instance.delete.return_value = self.mock_response

        # Execute
        result = execute_delete_request(self.test_url)

        # Assert
        self.assertEqual(result, self.mock_response)
        instance.delete.assert_called_once_with(self.test_url)

if __name__ == '__main__':
    unittest.main()