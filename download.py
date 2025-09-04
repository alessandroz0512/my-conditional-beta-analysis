import yfinance as yf
import pandas as pd

# ------------------------
# Step 1: Tickes & Market Index
# ------------------------
tickers = [
    "AAPL", "MSFT", "NVDA", "GOOGL", "META",
    "JPM", "BAC", "WFC", "C", "GS",
    "JNJ", "PFE", "MRK", "ABBV", "LLY",
    "CAT", "BA", "GE", "HON", "UNP",
    "AMZN", "TSLA", "HD", "MCD", "NKE",
    "XOM", "CVX", "COP", "SLB", "EOG",
    "PG", "KO", "PEP", "WMT", "COST"
]
market_index = "^GSPC"
all_tickers = tickers + [market_index]

# ------------------------
# Step 2: Download Prices
# ------------------------
raw = yf.download(all_tickers, start="2020-01-01", end="2025-01-01", group_by='ticker', auto_adjust=True)

# Save to CSV for reuse
raw.to_pickle("sp500_prices.pkl")
print("Download complete and saved to sp500_prices.pkl")
