import os
import json
import boto3
from datetime import datetime
from botocore.exceptions import ClientError

class DynamoDBService:
    def __init__(self, table_name):
        self.table_name = table_name
        self.dynamodb = boto3.resource('dynamodb')
        self.table = self.dynamodb.Table(table_name)

    def get_rates(self):
        try:
            response = self.table.scan()
            return response['Items']
        except ClientError as e:
            raise Exception(f"Error fetching rates from DynamoDB: {str(e)}")

def lambda_handler(event, context):
    dynamodb_service = DynamoDBService(os.environ['TABLE_NAME'])
    today = datetime.now().strftime('%Y-%m-%d')

    try:
        rates_data = dynamodb_service.get_rates()
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }

    rates = {}
    for item in rates_data:
        if item['Date'] == today:
            current_rate = item['Rate']
            previous_rate = item.get('PreviousRate', None)
            change = current_rate - previous_rate if previous_rate is not None else None
            rates[item['Currency']] = {
                'current': current_rate,
                'change': change
            }

    return {
        'statusCode': 200,
        'body': json.dumps({'rates': rates})
    }
