import os
import json
from dynamodb_service import DynamoDBService
from ecb_service import ECBService

def lambda_handler(event, context):
    ecb_service = ECBService()
    dynamodb_service = DynamoDBService(os.environ['TABLE_NAME'])

    try:
        data = ecb_service.fetch_exchange_rates()
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': f"Failed to fetch exchange rates: {str(e)}"})
        }

    current_date = ecb_service.get_current_date()

    for currency, rate in data['rates'].items():
        try:
            previous_rate = dynamodb_service.get_previous_rate(currency)
            dynamodb_service.update_rate(currency, rate, current_date, previous_rate)
        except Exception as e:
            return {
                'statusCode': 500,
                'body': json.dumps({'error': f"Failed to update rate for {currency}: {str(e)}"})
            }

    return {
        'statusCode': 200,
        'body': json.dumps('Rates fetched and updated successfully!')
    }
