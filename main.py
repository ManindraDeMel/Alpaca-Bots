import requests
import os
from dotenv import load_dotenv
import time
import json
from datetime import datetime, timedelta
import pytz
load_dotenv()

SUBSCRIPTION = False
SHORT_PERIOD = 1 # day/s
LONG_PERIOD = 5 # day/s
HISTORICAL_DATA = 4 # weeks for data retrieval 
API_KEY = os.getenv("APCA-API-KEY-ID")
API_SECRET_KEY = os.getenv("APCA-API-SECRET-KEY")
BASE_URL = 'https://data.alpaca.markets/v2'
ALPACA_ORDERS_URL = 'https://paper-api.alpaca.markets/v1/orders'
ALPACA_POSITIONS_URL = 'https://paper-api.alpaca.markets/v1/positions'
ALPACA_ACCOUNT_URL = 'https://paper-api.alpaca.markets/v1/account'

headers = {
    "APCA-API-KEY-ID": API_KEY,
    "APCA-API-SECRET-KEY": API_SECRET_KEY
}

stock_list = ['MSFT', 'AMZN', 'TSLA', 'GOOGL', 'AAPL']

def get_positions():
    try:
        response = requests.get(ALPACA_POSITIONS_URL, headers=headers)
        positions = response.json()
        return {position['symbol']: position for position in positions}
    except Exception as e:
        print(f"Error getting positions: {str(e)}\n")
        return {}

def get_account():
    try:
        response = requests.get(ALPACA_ACCOUNT_URL, headers=headers)
        account_info = response.json()
        return account_info
    except Exception as e:
        print(f"Error getting account information: {str(e)}\n")
        return None

def get_bars(stock):
    try:
        utc_now = datetime.now(pytz.UTC)  # Get current time in UTC

        if SUBSCRIPTION:
            end_time = utc_now
        else:
            end_time = utc_now - timedelta(minutes=16)

        start_time = end_time - timedelta(weeks=HISTORICAL_DATA) # adjust as needed

        start = start_time.strftime('%Y-%m-%dT%H:%M:%SZ')
        end = end_time.strftime('%Y-%m-%dT%H:%M:%SZ')

        response = requests.get(f'{BASE_URL}/stocks/{stock}/bars', headers=headers, 
                                params={"timeframe": '1D', 'start': start, 'end': end})
        data = response.json()
        if 'bars' in data:
            bars_data = data['bars']
            return bars_data
        else:
            print(f"No bars data for {stock}\n")
            return []
        
    except Exception as e:
        print(f"Error retrieving data for {stock}\n")
        print(str(e))
        return []

def get_moving_averages(stock, short_period=SHORT_PERIOD, long_period=LONG_PERIOD):
    bars = get_bars(stock)
    if len(bars) < long_period:
        return None, None

    short_period_prices = [bar['c'] for bar in bars[-short_period:]]
    long_period_prices = [bar['c'] for bar in bars[-long_period:]]

    short_ma = sum(short_period_prices) / short_period
    long_ma = sum(long_period_prices) / long_period

    return short_ma, long_ma

def place_order(stock, qty):
    try:
        order = {
            "symbol": stock,
            "qty": qty,
            "side": "buy",
            "type": "market",
            "time_in_force": "gtc"
        }
        r = requests.post(ALPACA_ORDERS_URL, headers=headers, json=order)
        print(f"Response: {json.dumps(r.json(), indent=2)}\n")
    except Exception as e:
        print(f"Error placing order: {str(e)}")

def sell_order(stock, qty):
    try:
        order = {
            "symbol": stock,
            "qty": qty,
            "side": "sell",
            "type": "market",
            "time_in_force": "gtc"
        }
        r = requests.post(ALPACA_ORDERS_URL, headers=headers, json=order)
        print(f"####\nSold order: {json.dumps(r.json(), indent=2)}\n")
    except Exception as e:
        print(f"Error selling order: {str(e)}\n")

def get_clock():
    try:
        response = requests.get('https://paper-api.alpaca.markets/v2/clock', headers=headers)
        clock_info = response.json()
        return clock_info
    except Exception as e:
        print(f"Error getting clock information: {str(e)}\n")
        return None

def is_market_open():
    clock_info = get_clock()
    if clock_info is not None:
        return clock_info['is_open']
    else:
        return False


def main():
    while True:
        if is_market_open():
                for stock in stock_list:
                    account_info = get_account()
                    if account_info is not None:
                        short_ma, long_ma = get_moving_averages(stock)
                        capital = min(100, float(account_info['cash']))  # adjust this to your capital
                        positions = get_positions()
                        if short_ma is None:
                            continue
                        if short_ma > long_ma:
                            if capital > 0:
                                place_order(stock, capital)
                                print(f"Buying {stock}\n")
                            else:
                                print(f"No Capital left to buy (Holding {stock}) \n")
                        elif short_ma < long_ma and stock in positions:
                            qty = int(positions[stock]['qty'])
                            if qty > 0:
                                sell_order(stock, qty)
                                print(f"Selling {stock}\n")
                            else:
                                print(f"No quantity of {stock} to sell")
                        else:
                            print(f"Holding position for stock: {stock}\n")
        else:
            print("Market is closed. Waiting for it to open...\n")
        time.sleep(60)

if __name__ == "__main__":
    main()
