import unittest
from unittest.mock import patch, Mock
from source.dynamodb_service import DynamoDBService
from botocore.exceptions import ClientError

class TestDynamoDBService(unittest.TestCase):

    def setUp(self):
        self.table_name = "ExchangeRates"
        self.dynamodb_service = DynamoDBService(self.table_name)

    @patch('dynamodb_service.boto3.resource')
    def test_get_previous_rate_success(self, mock_boto_resource):
        # Arrange
        mock_table = Mock()
        mock_boto_resource.return_value.Table.return_value = mock_table
        mock_table.get_item.return_value = {
            'Item': {'Currency': 'USD', 'Rate': 1.1}
        }

        # Act
        result = self.dynamodb_service.get_previous_rate('USD')

        # Assert
        self.assertEqual(result, 1.1)

    @patch('dynamodb_service.boto3.resource')
    def test_get_previous_rate_not_found(self, mock_boto_resource):
        # Arrange
        mock_table = Mock()
        mock_boto_resource.return_value.Table.return_value = mock_table
        mock_table.get_item.return_value = {
            'Item': None
        }

        # Act
        result = self.dynamodb_service.get_previous_rate('EUR')

        # Assert
        self.assertIsNone(result)

    @patch('dynamodb_service.boto3.resource')
    def test_get_previous_rate_failure(self, mock_boto_resource):
        # Arrange
        mock_table = Mock()
        mock_boto_resource.return_value.Table.return_value = mock_table
        mock_table.get_item.side_effect = ClientError(
            {"Error": {"Code": "ResourceNotFoundException", "Message": "Resource not found"}},
            "GetItem"
        )

        # Act & Assert
        with self.assertRaises(Exception) as context:
            self.dynamodb_service.get_previous_rate('GBP')
        self.assertIn("Error getting previous rate for GBP", str(context.exception))

    @patch('dynamodb_service.boto3.resource')
    def test_update_rate_success(self, mock_boto_resource):
        # Arrange
        mock_table = Mock()
        mock_boto_resource.return_value.Table.return_value = mock_table

        # Act
        self.dynamodb_service.update_rate('USD', 1.2, '2023-10-13', 1.1)

        # Assert
        mock_table.put_item.assert_called_once_with(Item={
            'Currency': 'USD',
            'Rate': 1.2,
            'Date': '2023-10-13',
            'PreviousRate': 1.1
        })

    @patch('dynamodb_service.boto3.resource')
    def test_update_rate_failure(self, mock_boto_resource):
        # Arrange
        mock_table = Mock()
        mock_boto_resource.return_value.Table.return_value = mock_table
        mock_table.put_item.side_effect = ClientError(
            {"Error": {"Code": "ConditionalCheckFailedException", "Message": "Conditional check failed"}},
            "PutItem"
        )

        # Act & Assert
        with self.assertRaises(Exception) as context:
            self.dynamodb_service.update_rate('EUR', 0.9, '2023-10-13', None)
        self.assertIn("Error updating rate for EUR", str(context.exception))

    @patch('dynamodb_service.boto3.resource')
    def test_get_rates_success(self, mock_boto_resource):
        # Arrange
        mock_table = Mock()
        mock_boto_resource.return_value.Table.return_value = mock_table
        mock_table.scan.return_value = {
            'Items': [
                {'Currency': 'USD', 'Rate': 1.1, 'Date': '2023-10-13'},
                {'Currency': 'EUR', 'Rate': 0.9, 'Date': '2023-10-13'}
            ]
        }

        # Act
        result = self.dynamodb_service.get_rates()

        # Assert
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]['Currency'], 'USD')

    @patch('dynamodb_service.boto3.resource')
    def test_get_rates_failure(self, mock_boto_resource):
        # Arrange
        mock_table = Mock()
        mock_boto_resource.return_value.Table.return_value = mock_table
        mock_table.scan.side_effect = ClientError(
            {"Error": {"Code": "InternalServerError", "Message": "Internal server error"}},
            "Scan"
        )

        # Act & Assert
        with self.assertRaises(Exception) as context:
            self.dynamodb_service.get_rates()
        self.assertIn("Error fetching rates from DynamoDB", str(context.exception))

if __name__ == '__main__':
    unittest.main()
