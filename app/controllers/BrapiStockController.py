import datetime
import requests

class BrapiStockController:
    def get_stocks(self) -> dict:
        url = "https://brapi.dev/api/available"
        response = requests.get(url)
        return response.json()

    def get_stock_info(self, ticker: str) -> dict:
        url = f"https://brapi.dev/api/quote/{ticker}?token=9D5sERcAW7br6f6eKbUnhL"
        params = {
            'range': '3mo',
            'interval': '1d',
            'fundamental': 'true'
        }
        response = requests.get(url, params=params)
        
        return self.__filtered_data(response.json())
    
    def __filtered_data(self, data: dict) -> dict:
        historical_data = data["results"][0]["historicalDataPrice"]
        for entry in historical_data:
            entry["date"] = self.__convert_timestamp_to_date_string(entry["date"])
        data["results"][0]["historicalDataPrice"] = historical_data
        return data
    
    @staticmethod
    def __convert_timestamp_to_date_string(timestamp) -> str:
        return datetime.datetime.fromtimestamp(timestamp, tz=datetime.timezone.utc).strftime('%d/%m/%Y')