import os
import unittest
from unittest.mock import patch, Mock
from source.get_exchange_rates import lambda_handler

class TestGetExchangeRates(unittest.TestCase):

    @patch('get_exchange_rates.DynamoDBService')
    def test_lambda_handler_success(self, mock_dynamodb_service):
        # Arrange
        os.environ['TABLE_NAME'] = 'ExchangeRates'
        mock_dynamodb_instance = mock_dynamodb_service.return_value
        mock_dynamodb_instance.get_rates.return_value = [
            {'Currency': 'USD', 'Rate': 1.1, 'Date': '2023-10-13', 'PreviousRate': 1.0},
            {'Currency': 'EUR', 'Rate': 0.9, 'Date': '2023-10-13', 'PreviousRate': 0.85},
            {'Currency': 'GBP', 'Rate': 0.8, 'Date': '2023-10-12'}  # Not today's date
        ]

        # Act
        response = lambda_handler({}, {})

        # Assert
        self.assertEqual(response['statusCode'], 200)
        response_body = json.loads(response['body'])
        self.assertIn('rates', response_body)
        self.assertEqual(len(response_body['rates']), 2)
        self.assertEqual(response_body['rates']['USD']['current'], 1.1)
        self.assertEqual(response_body['rates']['USD']['change'], 0.1)
        self.assertEqual(response_body['rates']['EUR']['current'], 0.9)
        self.assertEqual(response_body['rates']['EUR']['change'], 0.05)

    @patch('get_exchange_rates.DynamoDBService')
    def test_lambda_handler_fetch_failure(self, mock_dynamodb_service):
        # Arrange
        os.environ['TABLE_NAME'] = 'ExchangeRates'
        mock_dynamodb_instance = mock_dynamodb_service.return_value
        mock_dynamodb_instance.get_rates.side_effect = Exception("Fetch error")

        # Act
        response = lambda_handler({}, {})

        # Assert
        self.assertEqual(response['statusCode'], 500)
        self.assertIn("Fetch error", response['body'])

    @patch('get_exchange_rates.DynamoDBService')
    def test_lambda_handler_no_current_rates(self, mock_dynamodb_service):
        # Arrange
        os.environ['TABLE_NAME'] = 'ExchangeRates'
        mock_dynamodb_instance = mock_dynamodb_service.return_value
        mock_dynamodb_instance.get_rates.return_value = [
            {'Currency': 'USD', 'Rate': 1.1, 'Date': '2023-10-12'},
            {'Currency': 'EUR', 'Rate': 0.9, 'Date': '2023-10-12'}
        ]  # No rates for today's date

        # Act
        response = lambda_handler({}, {})

        # Assert
        self.assertEqual(response['statusCode'], 200)
        response_body = json.loads(response['body'])
        self.assertIn('rates', response_body)
        self.assertEqual(len(response_body['rates']), 0)  # No rates for today

if __name__ == '__main__':
    unittest.main()
