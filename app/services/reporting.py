import httpx
from app.models import ExtractedIntelligence
import logging

logger = logging.getLogger(__name__)

GUVI_CALLBACK_URL = "https://hackathon.guvi.in/api/updateHoneyPotFinalResult"

async def send_final_report(
    session_id: str,
    scam_detected: bool,
    total_messages: int,
    intelligence: ExtractedIntelligence,
    agent_notes: str
):
    try:
        payload = {
            "sessionId": session_id,
            "scamDetected": scam_detected,
            "totalMessagesExchanged": total_messages,
            "extractedIntelligence": intelligence.model_dump(),
            "agentNotes": agent_notes
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(GUVI_CALLBACK_URL, json=payload, timeout=10.0)
            
        if response.status_code == 200:
            logger.info(f"Successfully sent final report for {session_id}")
        else:
            logger.error(f"Failed to send report for {session_id}: {response.text}")
            
    except Exception as e:
        logger.error(f"Exception sending final report: {e}")
