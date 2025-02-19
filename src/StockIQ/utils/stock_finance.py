import yfinance as yf
from typing import Dict

def get_stock_financials(ticker: str) -> Dict:
    """Get Key financial metrics for a given stock ticker"""
    stock = yf.Ticker(ticker)

    try:
        financials = stock.financials

        return {
            "Revenue": financials.loc["Total Revenue"].to_dict() if "Total Revenue" in financials.index else {},
            "Net Income": financials.loc["Net Income"].to_dict() if "Net Income" in financials.index else {},
            "Operating Income": financials.loc["Operating Income"].to_dict() if "Operating Income" in financials.index else {}
        }
    
    except:
        return {
            "error": "Unable to fetch financial data"
        }