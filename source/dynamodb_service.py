import boto3
from botocore.exceptions import ClientError

class DynamoDBService:
    def __init__(self, table_name):
        self.table_name = table_name
        self.dynamodb = boto3.resource('dynamodb')
        self.table = self.dynamodb.Table(table_name)

    def get_previous_rate(self, currency):
        try:
            response = self.table.get_item(Key={'Currency': currency})
            return response.get('Item', {}).get('Rate', None)
        except ClientError as e:
            raise Exception(f"Error getting previous rate for {currency}: {str(e)}")

    def update_rate(self, currency, rate, date, previous_rate):
        try:
            self.table.put_item(Item={
                'Currency': currency,
                'Rate': rate,
                'Date': date,
                'PreviousRate': previous_rate
            })
        except ClientError as e:
            raise Exception(f"Error updating rate for {currency}: {str(e)}")

    def get_rates(self):
        try:
            response = self.table.scan()
            return response['Items']
        except ClientError as e:
            raise Exception(f"Error fetching rates from DynamoDB: {str(e)}")
