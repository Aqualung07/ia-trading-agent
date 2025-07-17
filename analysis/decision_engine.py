def generate_recommendation(fundamentals, tech_signal, score=None):
    """
    Generates a simplified recommendation based on fundamentals, technical signal and combined score.
    Prioritizes score if available.
    """
    pe = fundamentals.get("pe")
    eps = fundamentals.get("eps")
    revenue_growth = fundamentals.get("revenue_growth")
    profit_margin = fundamentals.get("profit_margin")
    debt = fundamentals.get("debt_to_equity")

    justifications = []  # Changed from justificaciones

    # Technical signal
    if tech_signal:
        if "RSI=" in tech_signal:
            try:
                rsi = float(tech_signal.split("RSI=")[1].split(",")[0])
                if rsi < 30:
                    justifications.append("oversold (low RSI)")
                elif rsi > 70:
                    justifications.append("overbought (high RSI)")
            except:
                pass
        if "MACD" in tech_signal:
            if "bullish" in tech_signal or "positive" in tech_signal:  # Changed from alcista/positivo
                justifications.append("MACD positive")
            elif "bearish" in tech_signal or "negative" in tech_signal:  # Changed from bajista/negativo
                justifications.append("MACD negative")

    # Fundamentals
    try:
        if eps is not None and float(eps) < 0:
            justifications.append("negative EPS")
        if revenue_growth:
            rev = float(revenue_growth.replace('%', '').strip())
            if rev > 20:
                justifications.append("strong growth")
    except:
        pass

    # Rules with score as main reference
    if score is not None:
        if score >= 2:
            action = "🟢 Accumulate"  # Changed from Acumular
        elif score == 1:
            action = "🟢 Hold"  # Changed from Mantener
        elif score == 0:
            action = "🟡 Watch closely"  # Changed from Observar de cerca
        else:
            action = "🔴 Reduce or Sell"  # Changed from Reducir o Vender
    else:
        # Fallback if no score
        # If we did not retrieve any fundamental metrics
        if not fundamentals:
            if tech_signal and ("RSI=" in tech_signal or "MACD" in tech_signal):
                return "🟡 Watch closely (interesting technicals, no fundamentals)"
            return "🔍 Watch (insufficient fundamental data)"
        action = "🟡 Watch"  # Changed from Observar

    summary = ", ".join(justifications) if justifications else "limited data"  # Changed from resumen/datos limitados
    return f"{action} ({summary})"
