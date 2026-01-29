from google import genai
from google.genai import types
from app.core.config import settings
import os

def test_new_client():
    print("Testing with new google-genai SDK...")
    client = genai.Client(api_key=settings.GEMINI_API_KEY)
    
    try:
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents="Hello, are you working?"
        )
        print(f"SUCCESS! Response: {response.text}")
    except Exception as e:
        print(f"FAILURE with new SDK: {e}")

if __name__ == "__main__":
    test_new_client()
