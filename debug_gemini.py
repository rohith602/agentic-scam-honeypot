import google.generativeai as genai
from app.core.config import settings
import asyncio

genai.configure(api_key=settings.GEMINI_API_KEY)

async def test_gemini():
    print("Listing Models...")
    try:
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                print(m.name)
    except Exception as e:
        print("List Models Failed:", e)

    print("\nTesting Gemini Connection...")
    # Try different names
    model_names = ['gemini-1.5-flash', 'models/gemini-1.5-flash']
    
    for name in model_names:
        print(f"\nTrying model: {name}")
        try:
            model = genai.GenerativeModel(name)
            response = model.generate_content("Hello")
            print(f"Success with {name}: {response.text}")
            break
        except Exception as e:
            print(f"Failed with {name}: {e}")

if __name__ == "__main__":
    asyncio.run(test_gemini())
