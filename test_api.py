import requests
import json
import time

# Use the key we just set in .env
API_KEY = "secure-honeypot-key-2026"
BASE_URL = "http://127.0.0.1:10000"

def test_root():
    # Simple ping if we had a root endpoint, but we only have webhook
    pass

def test_webhook_scam():
    url = f"{BASE_URL}/api/webhook"
    headers = {
        "x-api-key": API_KEY,
        "Content-Type": "application/json"
    }
    
    payload = {
        "sessionId": "test-session-123",
        "message": {
            "sender": "scammer",
            "text": "Your account is blocked. Click here to verify: http://evil.com/login",
            "timestamp": "2026-01-29T10:00:00Z"
        },
        "conversationHistory": [],
        "metadata": {
            "channel": "SMS",
            "language": "en"
        }
    }
    
    print(f"Testing Scam Message: {payload['message']['text']}")
    response = requests.post(url, headers=headers, json=payload)
    
    if response.status_code == 200:
        print("Success! Response:", response.json())
        data = response.json()
        if data.get("status") == "success" and data.get("reply"):
            print("PASS: Agent detected scam and replied.")
        else:
            print("FAIL: Agent did not reply as expected.")
    else:
        print(f"FAIL: Status Code {response.status_code}, Body: {response.text}")

def test_webhook_normal():
    url = f"{BASE_URL}/api/webhook"
    headers = {
        "x-api-key": API_KEY,
        "Content-Type": "application/json"
    }
    
    payload = {
        "sessionId": "test-session-456",
        "message": {
            "sender": "user",
            "text": "Hello, how are you?",
            "timestamp": "2026-01-29T10:00:00Z"
        },
        "conversationHistory": []
    }
    
    print(f"Testing Normal Message: {payload['message']['text']}")
    response = requests.post(url, headers=headers, json=payload)
    
    if response.status_code == 200:
        print("Success! Response:", response.json())
        data = response.json()
        if data.get("status") == "ignored":
            print("PASS: Agent correctly ignored non-scam.")
        else:
            print(f"FAIL: Agent response unexpected: {data}")
    else:
        print(f"FAIL: Status Code {response.status_code}, Body: {response.text}")

if __name__ == "__main__":
    # Wait for server to start if running in parallel (manual check strictly)
    print("Starting tests...")
    try:
        test_webhook_scam()
        test_webhook_normal()
    except Exception as e:
        print(f"Test failed with exception: {e}")
