import requests
from datetime import datetime

class ECBService:
    def __init__(self):
        self.url = "https://exchangerates.api.eurocentralbank.org/latest"

    def fetch_exchange_rates(self):
        try:
            response = requests.get(self.url)
            response.raise_for_status()  # Raise an error for bad responses
            return response.json()
        except requests.RequestException as e:
            raise Exception(f"Failed to fetch exchange rates: {str(e)}")

    def get_current_date(self):
        return datetime.now().strftime('%Y-%m-%d')
