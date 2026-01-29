import httpx
import asyncio
import json

async def test_scam_flow():
    url = "http://localhost:8000/api/v1/chat"
    headers = {"x-api-key": "secret-key"}
    
    # Payload 1: Initial Scam Message
    payload1 = {
        "sessionId": "test-session-123",
        "message": {
            "sender": "scammer",
            "text": "Your account is blocked. Verify now at http://fake-bank.com/login",
            "timestamp": "2026-01-21T10:15:30Z"
        },
        "conversationHistory": []
    }
    
    print("Sending Message 1...")
    async with httpx.AsyncClient() as client:
        resp = await client.post(url, json=payload1, headers=headers, timeout=60.0)
        print("Response 1:", json.dumps(resp.json(), indent=2))
        
        # Payload 2: Follow up with UPI
        payload2 = {
            "sessionId": "test-session-123",
            "message": {
                "sender": "scammer",
                "text": "Please pay to scammer@upi immediately.",
                "timestamp": "2026-01-21T10:16:30Z"
            },
            "conversationHistory": [
                payload1["message"],
                {"sender": "user", "text": "Oh no, what should I do?", "timestamp": "2026-01-21T10:16:00Z"}
            ]
        }
        
        print("\nSending Message 2...")
        resp2 = await client.post(url, json=payload2, headers=headers, timeout=60.0)
        print("Response 2:", json.dumps(resp2.json(), indent=2))

if __name__ == "__main__":
    asyncio.run(test_scam_flow())
