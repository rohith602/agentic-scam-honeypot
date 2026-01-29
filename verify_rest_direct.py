import requests
import os
from app.core.config import settings
import json

def test_rest_direct():
    api_key = settings.GEMINI_API_KEY
    # Try the standard v1beta endpoint for gemini-1.5-flash
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    
    headers = {"Content-Type": "application/json"}
    data = {
        "contents": [{
            "parts": [{"text": "Hello, are you working?"}]
        }]
    }
    
    print(f"Testing REST Endpoint: {url.split('?')[0]}...")
    try:
        response = requests.post(url, headers=headers, json=data)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
    except Exception as e:
        print(f"Request Error: {e}")

if __name__ == "__main__":
    test_rest_direct()
