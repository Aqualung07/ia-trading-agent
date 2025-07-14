from data.market_data import fetch_price_data
from analysis.tech_analysis import analyze_rsi_macd
from alerts.notify import send_alert
from analysis.fundamental_analysis import analyze_fundamentals
from analysis.decision_engine import generate_recommendation
from score import calculate_score
from llm_analysis import get_llm_analysis
from telegram_sender import send_telegram_message
import yaml

def load_config():
    with open("config.yaml", "r") as f:
        return yaml.safe_load(f)

def main(return_results=False, send_report=True):
    config = load_config()
    symbols = config.get("watchlist", [])
    
    results = []
    watchlist_activa = []

    for symbol in symbols:
        print(f"\n📊 Analizando {symbol}...")
        df = fetch_price_data(symbol)
        signal = analyze_rsi_macd(df, symbol)

        if signal:
            send_alert(symbol, signal)

        fundamentals = analyze_fundamentals(symbol)
        score = calculate_score(fundamentals, signal or "")
        recommendation = generate_recommendation(fundamentals, signal or "", score)

        results.append({
            "symbol": symbol,
            "tech": signal,
            "fundamentals": fundamentals,
            "score": score,
            "recommendation": recommendation
        })

        if "Observar de cerca" in recommendation:
            watchlist_activa.append(symbol)

    if send_report:
        markdown = get_llm_analysis(results)
        send_telegram_message(markdown)

    if return_results:
        return results, watchlist_activa

if __name__ == "__main__":
    main()
