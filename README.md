# Introduction
This script is for algorithmic trading using the Alpaca trading API. It checks a list of stocks, calculates their rate of change, and makes a buying decision based on the outcome. The script then watches the bought stocks and sells them when they have achieved a certain gain.

The script uses environment variables for the API key and secret key, which are loaded via the dotenv library.

# Prerequisites
To use this script, you will need:

- Python installed on your machine.
- A free account on Alpaca.
- Your Alpaca API Key ID and API Secret Key. These are provided by Alpaca when you create an account.
- The following Python libraries installed: requests, os, dotenv, time, json, threading. These can be installed via pip (Python's package installer). For example, to install requests, you would run pip install requests in your terminal.
An .env file in the same directory as your script. This file should contain your Alpaca API Key ID and Secret Key in the following format:
```
APCA-API-KEY-ID=yourapikeyid
APCA-API-SECRET-KEY=yoursecretkey
```
# Usage
First, ensure you've met all the prerequisites listed above.
Open your terminal and navigate to the directory where you have the script.
Run the script using the command python filename.py (replace "filename" with the actual name of your Python file).
Once running, the script will continuously check the rate of change of the defined stocks every minute. If the most recent closing price is greater than the second most recent closing price, it will place a buy order using Alpaca.

After placing a buy order, a new thread is created to watch that stock. If the price of that stock increases by 2% or more, it sells the stock and the thread ends.

## Important Disclaimer
This script is intended for educational purposes only. It is not intended as financial advice. The user is solely responsible for any trades made based on the execution of this script.

Trading in the stock market involves a substantial degree of risk, including the risk of losing more than your initial investment. 
The user of this script should carefully consider their financial condition, risk tolerance, and other relevant circumstances before deciding to implement this script for live trading.

By using this script, you agree that any monetary loss or gain incurred by its usage is not the responsibility of the author or any parties involved in the creation of the script.

