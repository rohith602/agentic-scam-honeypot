import google.generativeai as genai
from app.core.config import settings
import pprint

genai.configure(api_key=settings.GEMINI_API_KEY)

def check_methods():
    print("Checking model capabilities...")
    try:
        for m in genai.list_models():
            if 'gemini' in m.name:
                print(f"\nModel: {m.name}")
                print(f"Supported Methods: {m.supported_generation_methods}")
    except Exception as e:
        print(f"Error listing models: {e}")

if __name__ == "__main__":
    check_methods()
