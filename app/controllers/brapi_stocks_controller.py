import datetime
import requests

class BrapiStocksController:
    def get_stocks(self) -> dict:
        url = "https://brapi.dev/api/available"
        
        response = requests.get(url)
        response.raise_for_status()

        return response.json()

    def get_stock_info(self, ticker: str, time_range: str) -> dict:
        token ="9D5sERcAW7br6f6eKbUnhL"
        url = f"https://brapi.dev/api/quote/{ticker}?token={token}"
        params = {
            'range': time_range,
            'interval': '1d',
            'fundamental': True
        }

        response = requests.get(url, params=params)
        response.raise_for_status()

        return self.__filtered_data(response.json())
        
    
    def __filtered_data(self, data: dict) -> dict:
        historical_data = data["results"][0]["historicalDataPrice"]

        for entry in historical_data:
            entry["date"] = self.__convert_timestamp_to_date_string(entry["date"])
        data["results"][0]["historicalDataPrice"] = historical_data

        return data
    
    @staticmethod
    def __convert_timestamp_to_date_string(timestamp: int) -> str:
        return datetime.datetime.fromtimestamp(timestamp, tz=datetime.timezone.utc).strftime('%d/%m/%Y')