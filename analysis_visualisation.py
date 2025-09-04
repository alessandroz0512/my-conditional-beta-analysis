# ------------------------
# Imports
# ------------------------
import pandas as pd
import numpy as np
import yfinance as yf
import plotly.express as px
import plotly.graph_objects as go

# ------------------------
# Tickers and sector mapping
# ------------------------
tickers = [
    "XOM","CVX","COP","SLB",
    "LIN","DOW","NEM","ECL",
    "BA","CAT","HON","UNP",
    "AMZN","TSLA","HD","MCD",
    "PG","KO","PEP","WMT",
    "JNJ","PFE","MRK","ABBV",
    "JPM","BAC","WFC","C","GS",
    "AAPL","MSFT","NVDA","GOOG","META",
    "T","VZ","DIS","NFLX","CMCSA",
    "NEE","DUK","SO","AEP",
    "AMT","PLD","PSA","SPG"
]

sector_mapping = {
    "XOM":"Energy","CVX":"Energy","COP":"Energy","SLB":"Energy",
    "LIN":"Materials","DOW":"Materials","NEM":"Materials","ECL":"Materials",
    "BA":"Industrials","CAT":"Industrials","HON":"Industrials","UNP":"Industrials",
    "AMZN":"Consumer Discretionary","TSLA":"Consumer Discretionary",
    "HD":"Consumer Discretionary","MCD":"Consumer Discretionary",
    "PG":"Consumer Staples","KO":"Consumer Staples","PEP":"Consumer Staples","WMT":"Consumer Staples",
    "JNJ":"Healthcare","PFE":"Healthcare","MRK":"Healthcare","ABBV":"Healthcare",
    "JPM":"Financials","BAC":"Financials","WFC":"Financials","C":"Financials","GS":"Financials",
    "AAPL":"Information Technology","MSFT":"Information Technology","NVDA":"Information Technology",
    "GOOG":"Information Technology","META":"Information Technology",
    "T":"Communication Services","VZ":"Communication Services","DIS":"Communication Services",
    "NFLX":"Communication Services","CMCSA":"Communication Services",
    "NEE":"Utilities","DUK":"Utilities","SO":"Utilities","AEP":"Utilities",
    "AMT":"Real Estate","PLD":"Real Estate","PSA":"Real Estate","SPG":"Real Estate"
}

# ------------------------
# Data download and returns calculation
# ------------------------
price_data = {}
for t in tickers:
    try:
        data = yf.download(t, period="2y", interval="1d", progress=False, auto_adjust=True)
        if "Adj Close" in data.columns:
            adj = data["Adj Close"]
        else:
            adj = data.iloc[:,0]
        price_data[t] = adj
    except Exception as e:
        print(f"Could not download {t}: {e}")

prices = pd.DataFrame(price_data).dropna(how="all")
returns = prices.pct_change().dropna()

# Market returns: S&P500
market = yf.download("^GSPC", period="2y", interval="1d", progress=False, auto_adjust=True)
if "Adj Close" in market.columns:
    market_ret = market["Adj Close"].pct_change().dropna()
else:
    market_ret = market.iloc[:,0].pct_change().dropna()

# ------------------------
# Conditional Beta Function
# ------------------------
def conditional_beta(stock_ret, market_ret):
    up = market_ret > 0
    down = market_ret < 0
    if stock_ret[up].empty or stock_ret[down].empty:
        return np.nan, np.nan
    beta_plus = np.cov(stock_ret[up], market_ret[up])[0,1] / np.var(market_ret[up])
    beta_minus = np.cov(stock_ret[down], market_ret[down])[0,1] / np.var(market_ret[down])
    return beta_plus, beta_minus

# ------------------------
# Compute Beta+ and Beta- for all tickers
# ------------------------
results = []
for t in tickers:
    if t not in returns.columns:
        continue
    b_plus, b_minus = conditional_beta(returns[t], market_ret)
    results.append({
        "Ticker": t,
        "Sector": sector_mapping.get(t,"Unknown"),
        "Beta+": b_plus,
        "Beta-": b_minus,
        "Beta Ratio": b_plus / b_minus if b_minus != 0 else np.nan
    })

beta_df = pd.DataFrame(results)

# ------------------------
# Top 5 companies per sector
# ------------------------
top5_per_sector = beta_df.groupby("Sector").apply(lambda x: x.nlargest(5, "Beta+")).reset_index(drop=True)

# ------------------------
# Sector averages
# ------------------------
sector_avg = beta_df.groupby("Sector")[["Beta+", "Beta-", "Beta Ratio"]].mean().sort_values("Beta+")

# ------------------------
# ------------------------
# Visualization Section (all graphs)
# ------------------------
# 1) Sector Beta+ / Beta-
sector_avg_sorted = sector_avg.reset_index().sort_values("Beta+", ascending=False)
fig = go.Figure()
fig.add_trace(go.Bar(
    x=sector_avg_sorted["Beta+"],
    y=sector_avg_sorted["Sector"],
    orientation='h',
    name="Beta+",
    marker_color="#3498db",
    text=np.round(sector_avg_sorted["Beta+"],2)
))
fig.add_trace(go.Bar(
    x=sector_avg_sorted["Beta-"],
    y=sector_avg_sorted["Sector"],
    orientation='h',
    name="Beta-",
    marker_color="#e74c3c",
    text=np.round(sector_avg_sorted["Beta-"],2)
))
fig.update_layout(
    barmode='group',
    title="Average Beta+ and Beta- by Sector",
    xaxis_title="Beta",
    yaxis={'categoryorder':'total ascending'},
    bargap=0.2,
    height=600
)
fig.add_vline(x=1, line_dash="dash", line_color="black")
fig.show()

# 2) Sector Beta Ratio
sector_avg_ratio_sorted = sector_avg.reset_index().sort_values("Beta Ratio", ascending=False)
fig = px.bar(
    sector_avg_ratio_sorted,
    y="Sector",
    x="Beta Ratio",
    orientation='h',
    color="Beta Ratio",
    color_continuous_scale="Purples",
    text=np.round(sector_avg_ratio_sorted["Beta Ratio"],2),
    title="Average Beta+/Beta- Ratio by Sector",
    height=600
)
fig.update_layout(
    yaxis={'categoryorder':'total ascending'},
    xaxis_title="Beta+/Beta- Ratio",
    bargap=0.2
)
fig.add_vline(x=1, line_dash="dash", line_color="black")
fig.show()

# 3) Top 5 Companies per Sector Beta+ / Beta-
top5_sorted = top5_per_sector.sort_values("Beta+", ascending=False)
fig = go.Figure()
fig.add_trace(go.Bar(
    x=top5_sorted["Beta+"],
    y=top5_sorted["Ticker"],
    orientation='h',
    name="Beta+",
    marker_color="#3498db",
    text=np.round(top5_sorted["Beta+"],2),
    hovertext=top5_sorted["Sector"]
))
fig.add_trace(go.Bar(
    x=top5_sorted["Beta-"],
    y=top5_sorted["Ticker"],
    orientation='h',
    name="Beta-",
    marker_color="#e74c3c",
    text=np.round(top5_sorted["Beta-"],2),
    hovertext=top5_sorted["Sector"]
))
fig.update_layout(
    barmode='group',
    title="Top 5 Companies per Sector: Beta+ and Beta-",
    xaxis_title="Beta",
    yaxis={'categoryorder':'total ascending'},
    bargap=0.2,
    height=800
)
fig.add_vline(x=1, line_dash="dash", line_color="black")
fig.show()

# 4) Top 5 Companies per Sector Beta Ratio
top5_ratio_sorted = top5_per_sector.sort_values("Beta Ratio", ascending=False)
fig = px.bar(
    top5_ratio_sorted,
    y="Ticker",
    x="Beta Ratio",
    orientation='h',
    color="Beta Ratio",
    color_continuous_scale="Purples",
    text=np.round(top5_ratio_sorted["Beta Ratio"],2),
    hover_data=["Sector"],
    title="Top 5 Companies per Sector: Beta+/Beta- Ratio",
    height=800
)
fig.update_layout(
    yaxis={'categoryorder':'total ascending'},
    xaxis_title="Beta+/Beta- Ratio",
    bargap=0.2
)
fig.add_vline(x=1, line_dash="dash", line_color="black")
fig.show()
