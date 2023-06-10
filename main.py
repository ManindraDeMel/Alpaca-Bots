import requests
import os
from dotenv import load_dotenv
import time
import json
load_dotenv()

API_KEY = os.getenv("APCA-API-KEY-ID")
API_SECRET_KEY = os.getenv("APCA-API-SECRET-KEY")
BASE_URL = 'https://data.alpaca.markets/v2'
ALPACA_ORDERS_URL = 'https://paper-api.alpaca.markets/v1/orders'

headers = {
    "APCA-API-KEY-ID": API_KEY,
    "APCA-API-SECRET-KEY": API_SECRET_KEY
}

stock_list = ['AAPL', 'MSFT', 'AMZN', 'TSLA', 'GOOGL']

def get_bars(stock):
    try:
        response = requests.get(f'{BASE_URL}/stocks/{stock}/bars', headers=headers, params={"timeframe": '1Min'})
        data = response.json()
        if 'bars' in data:
            bars_data = data['bars']
            return bars_data
        else:
            print(f"No bars data for {stock}")
            return []
    except Exception as e:
        print(f"Error retrieving data for {stock}")
        print(str(e))
        return []

def get_moving_averages(stock, short_period=5, long_period=20):
    bars = get_bars(stock)
    if len(bars) < long_period:
        return None, None

    short_period_prices = [bar['c'] for bar in bars[-short_period:]]
    long_period_prices = [bar['c'] for bar in bars[-long_period:]]

    short_ma = sum(short_period_prices) / short_period
    long_ma = sum(long_period_prices) / long_period

    return short_ma, long_ma

def place_order(stock, capital):
    order = {
        "symbol": stock,
        "qty": capital,
        "side": "buy",
        "type": "market",
        "time_in_force": "gtc"
    }
    r = requests.post(ALPACA_ORDERS_URL, headers=headers, json=order)
    print(f"Placed order: {json.dumps(r.json(), indent=2)}")

def sell_order(stock, qty):
    order = {
        "symbol": stock,
        "qty": qty,
        "side": "sell",
        "type": "market",
        "time_in_force": "gtc"
    }
    r = requests.post(ALPACA_ORDERS_URL, headers=headers, json=order)
    print(f"Sold order: {json.dumps(r.json(), indent=2)}")

def main():
    while True:
        for stock in stock_list:
            short_ma, long_ma = get_moving_averages(stock)
            if short_ma is None:
                continue
            capital = 100  # adjust this to your capital
            if short_ma > long_ma:
                place_order(stock, capital)
                print(f"Buying {stock}")
            elif short_ma < long_ma:
                sell_order(stock, capital)
                print(f"Selling {stock}")
        time.sleep(60)

if __name__ == "__main__":
    main()
