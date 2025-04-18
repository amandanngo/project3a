# api_handling.py

import requests
from apikey_storage import get_api_key

def fetch_stock_data(symbol, function):
    """
    Fetch stock data from Alpha Vantage API.
    :param symbol: Stock symbol (e.g., 'AAPL')
    :param function: Time series function (e.g., 'TIME_SERIES_DAILY')
    :return: JSON data if successful, None otherwise
    """
    api_key = get_api_key()
    base_url = "https://www.alphavantage.co/query"


    if(function == "TIME_SERIES_INTRADAY"):
        params = {
        "function": function,
        "symbol": symbol,
        "apikey": api_key,
        "datatype": "json",
        "interval": "60min"
    }
    else:
        params = {
            "function": function,
            "symbol": symbol,
            "apikey": api_key,
            "datatype": "json"
        }

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()  # Will raise HTTPError for bad requests
        return response.json()
    except requests.exceptions.RequestException as e:
        print("Error fetching data:", e)
        return None
