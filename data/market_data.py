
import yfinance as yf
import pandas as pd

def fetch_price_data(symbol, period='6mo', interval='1d'):
    data = yf.download(symbol, period=period, interval=interval, auto_adjust=True)
    return data
