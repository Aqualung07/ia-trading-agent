
import pandas as pd

def analyze_rsi_macd(df, symbol):
    df = df.copy()
    df = df.dropna()  # elimina filas con NaNs, fundamental para evitar errores

    # Calculamos RSI
    delta = df['Close'].diff()
    gain = delta.where(delta > 0, 0)
    loss = -delta.where(delta < 0, 0)

    avg_gain = gain.rolling(window=14).mean()
    avg_loss = loss.rolling(window=14).mean()
    rs = avg_gain / avg_loss
    df['RSI'] = 100 - (100 / (1 + rs))

    # MACD
    df['EMA12'] = df['Close'].ewm(span=12).mean()
    df['EMA26'] = df['Close'].ewm(span=26).mean()
    df['MACD'] = df['EMA12'] - df['EMA26']
    df['Signal'] = df['MACD'].ewm(span=9).mean()

    # Eliminamos de nuevo filas con NaN (crucial antes de usar .iloc[-1])
    df = df.dropna()

    if df.empty:
        return None  # sin datos válidos, no analizamos

    latest = df.iloc[-1]

    try:
        rsi = float(pd.Series(latest['RSI']).iloc[0])
        macd = float(pd.Series(latest['MACD']).iloc[0])
        signal = float(pd.Series(latest['Signal']).iloc[0])
    except Exception as e:
        print(f"Error al convertir valores para {symbol}: {e}")
        return None

    if rsi < 30 or macd > signal:
        return f"Alert: {symbol} - RSI={rsi:.2f}, MACD crossover."
    return None

