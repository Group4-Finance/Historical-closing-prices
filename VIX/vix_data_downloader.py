# install yfinance
!pip install yfinance

import pandas as pd
import yfinance as yf
from datetime import datetime

# ticker for the VIX
vix_ticker = yf.Ticker("^VIX")

# Get today's date
today = datetime.today().strftime('%Y-%m-%d')

# Use the history method to fetch the data(DF)
vix_data = vix_ticker.history(start="2020-01-01", end=today)

# Resetting the index to have Date as a column
vix_data = vix_data.reset_index()

vix_data['Date'] = vix_data['Date'].dt.date

# Round the Close prices to 2 decimal places
vix_data['Close'] = vix_data['Close'].round(2)

# Selecting columns
vix_data = vix_data[['Date', 'Close']]

# Save the DB
vix_data.to_csv('vix_daily.csv')
