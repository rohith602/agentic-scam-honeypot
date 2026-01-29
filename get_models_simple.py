import google.generativeai as genai
from app.core.config import settings

genai.configure(api_key=settings.GEMINI_API_KEY)

def list_simple():
    try:
        models = genai.list_models()
        with open("simple_list.txt", "w", encoding="utf-8") as f:
            for m in models:
                if 'generateContent' in m.supported_generation_methods:
                    f.write(m.name + "\n")
        print("Done writing models.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    list_simple()
