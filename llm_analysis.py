import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_preferred_model():
    """Devuelve el mejor modelo disponible."""
    try:
        available_models = [m.id for m in client.models.list().data]
        for candidate in ["gpt-4o", "gpt-4", "gpt-3.5-turbo"]:
            if any(candidate in model for model in available_models):
                return candidate
        return None
    except Exception as e:
        print("⚠️ No se pudieron listar los modelos:", e)
        return None

def build_analysis_prompt(symbol, tech_signal, fundamentals, score=None):
    """Construye un prompt estructurado para análisis breve por activo."""
    return f"""
Actúa como un asesor financiero experto.

Analiza el activo {symbol} en base a los siguientes datos estructurados.

🔍 Señales técnicas:
{tech_signal}

📊 Datos fundamentales:
- P/E: {fundamentals.get('pe', 'N/A')}
- EPS: {fundamentals.get('eps', 'N/A')}
- Crecimiento de ingresos: {fundamentals.get('revenue_growth', 'N/A')}
- Margen de beneficio: {fundamentals.get('profit_margin', 'N/A')}
- Deuda/Capital: {fundamentals.get('debt_to_equity', 'N/A')}

📐 Score técnico-fundamental combinado: {score if score is not None else 'N/A'} (rango -3 a +3)

🎯 Tu tarea es:
1. Dar una única recomendación: Acumular / Mantener / Observar / Reducir / Vender
2. Resumir en 2 frases la justificación basada en los datos proporcionados

⚠️ No inventes información externa ni contexto adicional. Basa tu análisis únicamente en los datos anteriores.
"""

def get_llm_analysis(results):
    """Genera un informe corto por activo con recomendación y justificación concisa."""
    markdown = "# 📋 Recomendaciones resumidas por activo\n\n"
    model = get_preferred_model()

    if not model:
        return "❌ No tienes acceso a ningún modelo de lenguaje válido."

    for item in results:
        prompt = build_analysis_prompt(
            symbol=item['symbol'],
            tech_signal=item['tech'],
            fundamentals=item['fundamentals'],
            score=item.get('score')  # opcional
        )

        try:
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": "Eres un asesor financiero experto. Usa iconos para generar una estructura clara y fácil de leer."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3
            )
            answer = response.choices[0].message.content.strip()
            markdown += f"## {item['symbol']}\n{answer}\n\n"
        except Exception as e:
            markdown += f"## {item['symbol']}\n⚠️ Error al analizar con LLM: {e}\n\n"

    return markdown
