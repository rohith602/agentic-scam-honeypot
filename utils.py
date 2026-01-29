import requests
import os
from models import FinalCallbackPayload

CALLBACK_URL = "https://hackathon.guvi.in/api/updateHoneyPotFinalResult"

def send_final_result(payload: FinalCallbackPayload):
    """
    Sends the final extracted intelligence to the GUVI evaluation endpoint.
    """
    try:
        data = payload.model_dump()
        response = requests.post(
            CALLBACK_URL,
            json=data,
            timeout=10
        )
        response.raise_for_status()
        print(f"Successfully sent final result for session {payload.sessionId}")
        return True
    except requests.exceptions.RequestException as e:
        print(f"Error sending final result: {e}")
        return False
