# 📈 IA Trading Agent

An intelligent trading analysis tool that combines technical and fundamental analysis with AI-powered insights for stocks and ETFs.

## 🌟 Features

-   Technical analysis (RSI, MACD)
-   Fundamental data analysis using Yahoo Finance
-   AI-powered analysis using OpenAI GPT models
-   Scoring system for investment decisions
-   Telegram notifications
-   Support for international ETFs and stocks

## 🚀 Getting Started

1. Clone the repository
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Configure environment variables in `.env`:

```
OPENAI_API_KEY=your_openai_key
TELEGRAM_TOKEN=your_telegram_bot_token
TELEGRAM_CHAT_ID=your_chat_id
```

## 📊 Configuration

Edit `config.yaml` to customize your watchlist. Currently supports:

-   Global ETFs (IWDA.AS, SWDA.L, VWCE.DE)
-   US Market ETFs (CSPX.L, VTI, QQQ)
-   European and Emerging Markets (EUNL.DE, IEMG)
-   Bonds (BND, AGGH.AS)
-   REITs (VNQ)
-   Crypto ETFs (BITO, IBIT)
-   Gold ETFs (GLD, IAU)
-   Individual stocks (e.g., GUBRA.CO)

## 🔍 Analysis Components

-   `market_data.py`: Fetches price data using yfinance
-   `tech_analysis.py`: Calculates RSI and MACD indicators
-   `fundamental_analysis.py`: Retrieves key fundamental metrics
-   `decision_engine.py`: Generates trading recommendations
-   `score.py`: Calculates technical-fundamental combined scores
-   `llm_analysis.py`: Provides AI-powered market insights

## 📱 Notifications

The system sends alerts via Telegram when:

-   RSI reaches oversold/overbought levels
-   MACD shows significant crossovers
-   Combined score suggests strong buy/sell signals

## 🛠️ Usage

Run the main analysis:

```bash
python main.py
```

List available OpenAI models:

```bash
python list_models.py
```

## 📝 License

MIT License - See LICENSE file for details
