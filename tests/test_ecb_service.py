import unittest
from unittest.mock import patch, Mock
from source.ecb_service import ECBService
import requests


class TestECBService(unittest.TestCase):

    @patch('ecb_service.requests.get')
    def test_fetch_exchange_rates_success(self, mock_get):
        # Arrange
        service = ECBService()
        mock_response = Mock()
        mock_response.json.return_value = {
            "rates": {
                "USD": 1.1,
                "GBP": 0.9
            },
            "base": "EUR",
            "date": "2023-10-13"
        }
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        # Act
        result = service.fetch_exchange_rates()

        # Assert
        self.assertEqual(result['rates']['USD'], 1.1)
        self.assertEqual(result['base'], "EUR")
        self.assertEqual(result['date'], "2023-10-13")

    @patch('ecb_service.requests.get')
    def test_fetch_exchange_rates_failure(self, mock_get):
        # Arrange
        service = ECBService()
        mock_get.side_effect = requests.exceptions.HTTPError("HTTP Error")

        # Act & Assert
        with self.assertRaises(Exception) as context:
            service.fetch_exchange_rates()
        self.assertIn("Failed to fetch exchange rates", str(context.exception))

    def test_get_current_date(self):
        # Arrange
        service = ECBService()

        # Act
        result = service.get_current_date()

        # Assert
        # We just check if the result matches the expected date format
        self.assertRegex(result, r'\d{4}-\d{2}-\d{2}')  # Matches YYYY-MM-DD


if __name__ == '__main__':
    unittest.main()
