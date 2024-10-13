import pytest
import requests

BASE_URL = "https://your-api-gateway-url/exchange-rates"  # Replace with your actual API Gateway URL

@pytest.fixture(scope='module', autouse=True)
def setup_module():
    # Optionally set up any resources needed for the tests
    yield
    # Optionally tear down any resources after tests are completed

def test_get_exchange_rates_success():
    response = requests.get(BASE_URL)

    assert response.status_code == 200
    response_data = response.json()
    assert 'rates' in response_data
    assert isinstance(response_data['rates'], dict)

def test_get_exchange_rates_no_rates():
    # You may need to clear the DynamoDB or set it to a state where there are no rates for today.
    # For the sake of this example, let's assume you have a way to ensure this.

    # Trigger the condition where there are no current rates.
    response = requests.get(BASE_URL)

    assert response.status_code == 200
    response_data = response.json()
    assert 'rates' in response_data
    assert len(response_data['rates']) == 0

def test_fetch_exchange_rates_integration():
    # This test assumes that your fetching function will run and populate the database correctly.
    fetch_url = "https://your-api-gateway-url/fetch-exchange-rates"  # Replace with your actual fetch URL
    response = requests.post(fetch_url)

    assert response.status_code == 200
    assert "Rates fetched and updated successfully!" in response.text

    # Verify that the rates are now available
    rates_response = requests.get(BASE_URL)
    assert rates_response.status_code == 200
    rates_data = rates_response.json()
    assert 'rates' in rates_data
    assert isinstance(rates_data['rates'], dict)

if __name__ == '__main__':
    pytest.main()
