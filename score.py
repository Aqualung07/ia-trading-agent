def parse_float(val):
    """
    Convierte un valor a float si es posible, si no devuelve None.
    """
    if val is None:
        return None
    if isinstance(val, str):
        val = val.replace('%', '').strip()
        if val.lower() in ['n/a', 'none', '-', '']:
            return None
    try:
        return float(val)
    except (ValueError, TypeError):
        return None

def calculate_score(fundamentals: dict, tech: str) -> int:
    """
    Calcula un score técnico-fundamental simple basado en reglas heurísticas.
    Rango sugerido: de -3 (muy negativo) a +3 (muy positivo)
    """
    score = 0

    # Fundamentos
    pe = parse_float(fundamentals.get("pe"))
    if pe is not None:
        if pe > 0 and pe < 20:
            score += 1
        elif pe > 30:
            score -= 1

    eps = parse_float(fundamentals.get("eps"))
    if eps is not None:
        if eps > 0:
            score += 1
        elif eps < 0:
            score -= 1

    growth = parse_float(fundamentals.get("revenue_growth"))
    if growth is not None and growth > 15:
        score += 1

    margin = parse_float(fundamentals.get("profit_margin"))
    if margin is not None and margin < 0:
        score -= 1

    debt = parse_float(fundamentals.get("debt_to_equity"))
    if debt is not None and debt > 100:
        score -= 1

    # Técnica
    if "RSI=" in tech:
        try:
            rsi_val = float(tech.split("RSI=")[1].split(",")[0])
            if rsi_val < 30:
                score += 1
            elif rsi_val > 70:
                score -= 1
        except:
            pass

    if "MACD alcista" in tech or "MACD positivo" in tech:
        score += 1
    elif "MACD bajista" in tech or "MACD negativo" in tech:
        score -= 1

    return score
