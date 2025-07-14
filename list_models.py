from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def list_available_models():
    try:
        models = client.models.list()
        print("📦 Modelos disponibles con tu API key:")
        for model in models.data:
            print("-", model.id)
    except Exception as e:
        print("⚠️ Error al listar modelos:", e)

if __name__ == "__main__":
    list_available_models()
