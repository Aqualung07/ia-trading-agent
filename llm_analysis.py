import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_preferred_model():
    """Returns the best available model."""
    try:
        available_models = [m.id for m in client.models.list().data]
        for candidate in ["gpt-4o", "gpt-4", "gpt-3.5-turbo"]:
            if any(candidate in model for model in available_models):
                return candidate
        return None
    except Exception as e:
        print("⚠️ Could not list models:", e)
        return None

def build_analysis_prompt(symbol, tech_signal, fundamentals, score=None):
    """Builds a structured prompt for brief asset analysis."""
    return f"""
Act as a financial expert advisor.

Analyze the asset {symbol} based on the following structured data.

🔍 Technical signals:
{tech_signal}

📊 Fundamental data:
- P/E: {fundamentals.get('pe', 'N/A')}
- EPS: {fundamentals.get('eps', 'N/A')}
- Revenue Growth: {fundamentals.get('revenue_growth', 'N/A')}
- Profit Margin: {fundamentals.get('profit_margin', 'N/A')}
- Debt/Equity: {fundamentals.get('debt_to_equity', 'N/A')}

📐 Combined technical-fundamental score: {score if score is not None else 'N/A'} (range -3 to +3)

🎯 Your task is:
1. Give a single recommendation: Accumulate / Hold / Watch / Reduce / Sell
2. Summarize in 2 sentences the justification based on provided data

⚠️ Don't make up external information or additional context. Base your analysis only on the data above.
"""

def get_llm_analysis(results):
    """Generates a short report per asset with recommendation and concise justification."""
    markdown = "# 📋 Recommendations summarized by asset\n\n"
    model = get_preferred_model()

    if not model:
        return "❌ You do not have access to any valid language model."

    for item in results:
        prompt = build_analysis_prompt(
            symbol=item['symbol'],
            tech_signal=item['tech'],
            fundamentals=item['fundamentals'],
            score=item.get('score')  # optional
        )

        try:
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": "You are a financial expert advisor. Use icons to generate a clear and easy-to-read structure."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3
            )
            answer = response.choices[0].message.content.strip()
            markdown += f"## {item['symbol']}\n{answer}\n\n"
        except Exception as e:
            markdown += f"## {item['symbol']}\n⚠️ Error analyzing with LLM: {e}\n\n"

    return markdown
