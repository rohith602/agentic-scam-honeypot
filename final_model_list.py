import google.generativeai as genai
from app.core.config import settings
import sys

# Force UTF-8 encoding for output
sys.stdout.reconfigure(encoding='utf-8')

genai.configure(api_key=settings.GEMINI_API_KEY)

def list_valid_models():
    print("Listing models that support 'generateContent':")
    print("-" * 50)
    try:
        count = 0
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                print(f"Model: {m.name}")
                count += 1
        
        if count == 0:
            print("No models found with 'generateContent' capability.")
        else:
            print("-" * 50)
            print(f"Found {count} capable models.")
            
    except Exception as e:
        print(f"Error listing models: {e}")

if __name__ == "__main__":
    list_valid_models()
