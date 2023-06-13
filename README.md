# Introduction
This script is an algorithmic trading bot that utilizes the Alpaca trading API to make buy/sell decisions based on moving averages (a common technical analysis strategy). Specifically, it uses the concept of crossover between short-term and long-term moving averages as a signal for buying and selling.

# Prerequisites
To use this script, you will need:

- Python installed on your machine.
- A free account on Alpaca.
- Your Alpaca API Key ID and API Secret Key. These are provided by Alpaca when you create an account.
- The following Python libraries installed: requests, os, dotenv, time, json, datetime, pytz. These can be installed via pip (Python's package installer). For example, to install requests, you would run `pip install requests` in your terminal.
An .env file in the same directory as your script. This file should contain your Alpaca API Key ID and Secret Key in the following format:
```
APCA-API-KEY-ID=yourapikeyid
APCA-API-SECRET-KEY=yoursecretkey
```
# Usage
First, ensure you've met all the prerequisites listed above.
Open your terminal and navigate to the directory where you have the script.
Run the script using the command python filename.py (replace "filename" with the actual name of your Python file).
Once running, the script will continuously check the rate of change of the defined stocks every minute. If the short-term moving average crosses above the long-term moving average, it is a signal to buy. Conversely, if the short-term moving average crosses below the long-term moving average, it's a signal to sell.

The script also checks if the market is open before executing any buy/sell orders.

## Important Disclaimer
This script is intended for educational purposes only. It is not intended as financial advice. The user is solely responsible for any trades made based on the execution of this script.

Trading in the stock market involves a substantial degree of risk, including the risk of losing more than your initial investment. The user of this script should carefully consider their financial condition, risk tolerance, and other relevant circumstances before deciding to implement this script for live trading.

By using this script, you agree that any monetary loss or gain incurred by its usage is not the responsibility of the author or any parties involved in the creation of the script.
