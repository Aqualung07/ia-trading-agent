import yfinance as yf

def analyze_fundamentals(symbol):
    stock = yf.Ticker(symbol)
    info = stock.info

    pe = info.get("trailingPE")
    eps = info.get("trailingEps")
    revenue_growth = info.get("revenueGrowth")
    profit_margin = info.get("profitMargins")
    debt_to_equity = info.get("debtToEquity")

    if all(v is None for v in [pe, eps, revenue_growth, profit_margin, debt_to_equity]):
        return {}

    return {
        "symbol": symbol,
        "pe": pe,
        "eps": eps,
        "revenue_growth": f"{revenue_growth:.2%}" if revenue_growth is not None else None,
        "profit_margin": f"{profit_margin:.2%}" if profit_margin is not None else None,
        "debt_to_equity": debt_to_equity
    }
