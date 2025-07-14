from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def list_available_models():
    try:
        models = client.models.list()
        print("📦 Available models with your API key:")
        for model in models.data:
            print("-", model.id)
    except Exception as e:
        print("⚠️ Error listing models:", e)

if __name__ == "__main__":
    list_available_models()
