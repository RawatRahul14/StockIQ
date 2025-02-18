import yfinance as yf
from typing import Dict

def get_stock_data(ticker: str) -> Dict:
    stock = yf.Ticker(ticker)
    info = stock.info

    return {
        "currentPrice": info.get("currentPrice"),
        "marketCap": info.get("marketCap"),
        "longName": info.get("longName"),
        "sector": info.get("sector"),
        "industry": info.get("industry"),
        "website": info.get("website"),
        "longBusinessSummary": info.get("longBusinessSummary")
    }