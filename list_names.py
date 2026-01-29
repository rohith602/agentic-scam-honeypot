import httpx
import asyncio
from app.core.config import settings
import json

async def list_models_names():
    api_key = settings.GEMINI_API_KEY
    url = f"https://generativelanguage.googleapis.com/v1beta/models?key={api_key}"
    
    async with httpx.AsyncClient() as client:
        resp = await client.get(url)
        data = resp.json()
        if 'models' in data:
            for m in data['models']:
                if 'generateContent' in m.get('supportedGenerationMethods', []):
                    print(f"FOUND_MODEL: {m['name']}")
        else:
            print("No models found in response")

if __name__ == "__main__":
    asyncio.run(list_models_names())
