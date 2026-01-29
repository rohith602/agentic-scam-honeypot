import google.generativeai as genai
from app.core.config import settings
import asyncio

genai.configure(api_key=settings.GEMINI_API_KEY)

async def test_gen():
    print("Testing Generation...")
    
    candidates = [
        'models/gemini-1.5-flash',
        'models/gemini-1.5-flash-001',
        'models/gemini-1.5-flash-8b',
        'models/gemini-1.5-pro',
        'models/gemini-1.0-pro'
    ]
    
    for name in candidates:
        print(f"\nTrying {name}...")
        try:
            model = genai.GenerativeModel(name)
            response = model.generate_content("Hello")
            print(f"SUCCESS with {name}! Output: {response.text}")
            return
        except Exception as e:
            print(f"FAILURE with {name}: {e}")

if __name__ == "__main__":
    asyncio.run(test_gen())
