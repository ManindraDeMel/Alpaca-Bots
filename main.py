import requests
import os
from dotenv import load_dotenv
import time
import json
import threading
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
    response = requests.get(f'{BASE_URL}/stocks/{stock}/bars', headers=headers, params={"timeframe": '1Min'})
    data = response.json()
    bars_data = data['bars']
    return bars_data

def calculate_roc(stock_list):
    roc_values = {}
    for stock in stock_list:
        try:
            bars = get_bars(stock)
            if len(bars) >= 2:
                current_price = bars[-1]['c']
                past_price = bars[-2]['c']
                roc = ((current_price - past_price) / past_price) * 100
                roc_values[stock] = roc
            else:
                print(f"Not enough data for {stock}")
        except Exception as e:
            print(f"Error retrieving data for {stock}")
            print(str(e))
    sorted_roc = sorted(roc_values.items(), key=lambda x: x[1], reverse=True)
    return sorted_roc

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

def get_current_price(stock):
    response = requests.get(f'{BASE_URL}/stocks/{stock}/bars', headers=headers, params={"timeframe": '1Min'})
    data = response.json()
    current_price = data['bars'][-1]['c']
    return current_price

def check_and_sell(stock, qty, bought_price):
    while True:
        print(f"Waiting to sell: {stock}\n")
        current_price = get_current_price(stock)
        if ((current_price - bought_price) / bought_price) >= 0.02:
            sell_order(stock, qty)
            print(f"Selling {stock}")
            break
        time.sleep(60)

def main():
    while True:
        sorted_roc = calculate_roc(stock_list)
        for stock, roc in sorted_roc:
            barset = get_bars(stock)
            ask_price = barset[-1]['c']  # get the close price of the last bar
            last_traded_price = barset[-2]['c']  # get the close price of the second last bar
            if ask_price > last_traded_price:
                capital = 100  # adjust this to your capital
                place_order(stock, capital)
                print(f"Buying {stock}")
                thread = threading.Thread(target=check_and_sell, args=(stock, capital, ask_price))
                thread.start()
        time.sleep(60)


if __name__ == "__main__":
    main()