import google.generativeai as genai
from app.core.config import settings
import asyncio

genai.configure(api_key=settings.GEMINI_API_KEY)

async def test_pro():
    print("Testing gemini-pro...")
    try:
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content("Hello, are you there?")
        print(f"Success: {response.text}")
    except Exception as e:
        print(f"Failed: {e}")

if __name__ == "__main__":
    asyncio.run(test_pro())
