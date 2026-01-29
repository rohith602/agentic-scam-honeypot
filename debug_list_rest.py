import httpx
import asyncio
from app.core.config import settings

async def list_models_rest():
    api_key = settings.GEMINI_API_KEY
    url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"
    
    print(f"Listing models for key ...{api_key[-4:]}")
    async with httpx.AsyncClient() as client:
        resp = await client.get(url)
        print(f"Status: {resp.status_code}")
        print(f"Response: {resp.text}")

if __name__ == "__main__":
    asyncio.run(list_models_rest())
