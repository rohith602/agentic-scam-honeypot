import google.generativeai as genai
from app.core.config import settings
import asyncio

genai.configure(api_key=settings.GEMINI_API_KEY)

async def bruteforce():
    candidates = [
        "gemini-1.5-flash",
        "models/gemini-1.5-flash",
        "gemini-1.5-flash-001",
        "models/gemini-1.5-flash-001",
        "gemini-1.5-flash-8b",
        "models/gemini-1.5-flash-8b",
        "gemini-1.5-pro",
        "models/gemini-1.5-pro",
        "gemini-pro",
        "models/gemini-pro",
        "gemini-1.0-pro",
        "models/gemini-1.0-pro"
    ]
    
    print("Starting Brute Force...")
    for name in candidates:
        print(f"Trying {name}...", end=" ")
        try:
            model = genai.GenerativeModel(name)
            resp = model.generate_content("Hi")
            print(f"SUCCESS! Output: {resp.text}")
            with open("working_model.txt", "w") as f:
                f.write(name)
            return
        except Exception as e:
            print(f"Fail: {e}")

if __name__ == "__main__":
    asyncio.run(bruteforce())
