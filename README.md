# Currency Exchange Tracker

## Overview
This project provides a currency exchange tracker that fetches rates from the European Central Bank, stores them in DynamoDB, and exposes them via a REST API.

## Requirements
boto3
pytest(to run integration tests)

## Directory Structure
currency_exchange_tracker/
├── lambda/ 
    │ ├── init.py │ 
    ├── fetch_exchange_rates.py │ 
    ├── dynamodb_service.py │ └── ecb_service.py
├── tests/
    ├── test_fetch_exchange_rates.py
    ├── test_dynamodb_service.py
    └── test_ecb_service.py
    └── test_get_exchange_rates.py
    └── test_integration.py
├── template.yaml
└── README.md


## Setup Instructions


## Setup Instructions

### Prerequisites
- AWS CLI installed and configured.
- Python 3.x installed.

### Deploying the Application

1. **Create CloudFormation Stack**:
   - Save the `template.yaml` file.
   - Deploy the stack:
     ```
     aws cloudformation deploy --template-file template.yaml --stack-name CurrencyExchangeStack --capabilities CAPABILITY_IAM
     ```

2. **Upload Lambda Code**:
   - Ensure that the Lambda function code is included in the CloudFormation template. You can zip the files and upload them if needed.

3. **Testing the API**:
   - After deployment, test the API endpoint:
     ```
     curl https://<api-id>.execute-api.<region>.amazonaws.com/prod/exchange-rates
     ```

## API Endpoints

Step 1: Get the API Gateway URL
After deploying your CloudFormation stack, you will receive an API Gateway URL. You can find it in the AWS Management Console under the API Gateway section or in the outputs of your CloudFormation stack.

Step 2: Test the APIs
1. Fetch Current Exchange Rates
API Endpoint:
    GET https://<api-id>.execute-api.<region>.amazonaws.com/prod/exchange-rates
2. Testing with curl:
   ```
   curl -X GET https://<api-id>.execute-api.<region>.amazonaws.com/prod/exchange-rates
   ```
Sample Response:
When the request is successful, you might receive a response like this:
```
{
  "rates": {
    "USD": {
      "current": 1.1,
      "change": -0.02
    },
    "GBP": {
      "current": 0.85,
      "change": 0.01
    },
    "JPY": {
      "current": 120.0,
      "change": 1.5
    }
  }
}
```

3.Check for Errors
You may also want to test how the API responds to various error conditions. Here are some examples of what could happen:

Case 1: ECB Service Unavailable
If the ECB service is down or there’s an issue fetching rates, the response might look like this:
```
{
  "error": "Failed to fetch exchange rates: <error details>"
}
```

Case 2: Database Issues
If there’s an issue with the DynamoDB table (like it doesn’t exist or the permissions are wrong), you might see:
```
{
  "error": "Error fetching rates from DynamoDB: <error details>"
}
```
4.To Run the unittests:
```
python -m unittest discover -s lambda -p "test_*.py"
```
5.To Run the integration tests:
```
pytest test_integration.py

```

Additional Notes
Permissions: Ensure that the Lambda function has the necessary permissions to read/write to DynamoDB and that the API Gateway can invoke the Lambda function.
Monitoring: Use AWS CloudWatch logs to monitor the Lambda function's execution for debugging purposes.