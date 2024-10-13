import os
import unittest
from unittest.mock import patch, Mock
from source.fetch_exchange_rates import lambda_handler


class TestFetchExchangeRates(unittest.TestCase):

    @patch('fetch_exchange_rates.ECBService')
    @patch('fetch_exchange_rates.DynamoDBService')
    def test_lambda_handler_success(self, mock_dynamodb_service, mock_ecb_service):
        # Arrange
        os.environ['TABLE_NAME'] = 'ExchangeRates'
        mock_ecb_instance = mock_ecb_service.return_value
        mock_dynamodb_instance = mock_dynamodb_service.return_value

        mock_ecb_instance.fetch_exchange_rates.return_value = {
            "rates": {
                "USD": 1.1,
                "EUR": 1.0
            }
        }
        mock_ecb_instance.get_current_date.return_value = "2023-10-13"

        mock_dynamodb_instance.get_previous_rate.side_effect = [1.0, None]  # Previous rates for USD and EUR

        # Act
        response = lambda_handler({}, {})

        # Assert
        self.assertEqual(response['statusCode'], 200)
        self.assertIn('Rates fetched and updated successfully!', response['body'])
        mock_dynamodb_instance.update_rate.assert_any_call('USD', 1.1, '2023-10-13', 1.0)
        mock_dynamodb_instance.update_rate.assert_any_call('EUR', 1.0, '2023-10-13', None)

    @patch('fetch_exchange_rates.ECBService')
    @patch('fetch_exchange_rates.DynamoDBService')
    def test_lambda_handler_fetch_failure(self, mock_dynamodb_service, mock_ecb_service):
        # Arrange
        os.environ['TABLE_NAME'] = 'ExchangeRates'
        mock_ecb_instance = mock_ecb_service.return_value
        mock_ecb_instance.fetch_exchange_rates.side_effect = Exception("Fetch error")

        # Act
        response = lambda_handler({}, {})

        # Assert
        self.assertEqual(response['statusCode'], 500)
        self.assertIn("Failed to fetch exchange rates", response['body'])

    @patch('fetch_exchange_rates.ECBService')
    @patch('fetch_exchange_rates.DynamoDBService')
    def test_lambda_handler_update_failure(self, mock_dynamodb_service, mock_ecb_service):
        # Arrange
        os.environ['TABLE_NAME'] = 'ExchangeRates'
        mock_ecb_instance = mock_ecb_service.return_value
        mock_dynamodb_instance = mock_dynamodb_service.return_value

        mock_ecb_instance.fetch_exchange_rates.return_value = {
            "rates": {
                "USD": 1.1
            }
        }
        mock_ecb_instance.get_current_date.return_value = "2023-10-13"
        mock_dynamodb_instance.get_previous_rate.return_value = 1.0
        mock_dynamodb_instance.update_rate.side_effect = Exception("Update error")

        # Act
        response = lambda_handler({}, {})

        # Assert
        self.assertEqual(response['statusCode'], 500)
        self.assertIn("Failed to update rate for USD", response['body'])


if __name__ == '__main__':
    unittest.main()
