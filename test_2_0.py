import google.generativeai as genai
from app.core.config import settings
import sys

# Force UTF-8 encoding for output
sys.stdout.reconfigure(encoding='utf-8')

genai.configure(api_key=settings.GEMINI_API_KEY)

def test_2_0():
    model_name = 'models/gemini-2.0-flash'
    print(f"Testing {model_name}...")
    try:
        model = genai.GenerativeModel(model_name)
        response = model.generate_content("Hello! Are you working?")
        print(f"SUCCESS! Response: {response.text}")
    except Exception as e:
        print(f"FAILURE with {model_name}: {e}")

if __name__ == "__main__":
    test_2_0()
