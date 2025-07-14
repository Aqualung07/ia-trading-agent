
def generate_recommendation(fundamentals, tech_signal, score=None):
    """
    Genera una recomendación simplificada en base a fundamentos, señal técnica y un score combinado.
    Prioriza score si está disponible.
    """
    pe = fundamentals.get("pe")
    eps = fundamentals.get("eps")
    revenue_growth = fundamentals.get("revenue_growth")
    profit_margin = fundamentals.get("profit_margin")
    debt = fundamentals.get("debt_to_equity")

    justificaciones = []

    # Señal técnica
    if tech_signal:
        if "RSI=" in tech_signal:
            try:
                rsi = float(tech_signal.split("RSI=")[1].split(",")[0])
                if rsi < 30:
                    justificaciones.append("sobrevendido (RSI bajo)")
                elif rsi > 70:
                    justificaciones.append("sobrecomprado (RSI alto)")
            except:
                pass
        if "MACD" in tech_signal:
            if "alcista" in tech_signal or "positivo" in tech_signal:
                justificaciones.append("MACD positivo")
            elif "bajista" in tech_signal or "negativo" in tech_signal:
                justificaciones.append("MACD negativo")

    # Fundamentales
    try:
        if eps is not None and float(eps) < 0:
            justificaciones.append("EPS negativo")
        if revenue_growth:
            rev = float(revenue_growth.replace('%', '').strip())
            if rev > 20:
                justificaciones.append("fuerte crecimiento")
    except:
        pass

    # Reglas con score como referencia principal
    if score is not None:
        if score >= 2:
            accion = "🟢 Acumular"
        elif score == 1:
            accion = "🟢 Mantener"
        elif score == 0:
            accion = "🟡 Observar de cerca"
        else:
            accion = "🔴 Reducir o Vender"
    else:
        # Fallback si no hay score
        if "Sin datos fundamentales" in fundamentals:
            if tech_signal and ("RSI=" in tech_signal or "MACD" in tech_signal):
                return "🟡 Observar de cerca (técnico interesante, sin fundamentos)"
            return "🔍 Observar (sin datos fundamentales suficientes)"
        accion = "🟡 Observar"

    resumen = ", ".join(justificaciones) if justificaciones else "datos limitados"
    return f"{accion} ({resumen})"
