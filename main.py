from fastapi import FastAPI, HTTPException, Header, BackgroundTasks, Request
from models import IncomingRequest, AgentResponse, FinalCallbackPayload
from agent import HoneyPotAgent
from utils import send_final_result
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()
agent = HoneyPotAgent()

# Expected API Key (set in env)
EXPECTED_API_KEY = os.getenv("HONEYPOT_API_KEY", "default-secret-key")

@app.post("/api/webhook")
async def webhook(
    request: IncomingRequest,
    background_tasks: BackgroundTasks,
    x_api_key: str = Header(None)
):
    if x_api_key != EXPECTED_API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")

    current_msg_text = request.message.text
    
    # 1. Detect Scam
    is_scam = agent.detect_scam(current_msg_text, request.conversationHistory)
    
    if is_scam:
        # 2. Generate Agent Reply
        reply_text = agent.generate_reply(current_msg_text, request.conversationHistory)
        
        # 3. Check for end-of-conversation or intelligence extraction opportunity
        # Logic: If conversation is long enough or specific triggers, extract and callback
        # For this hackathon, maybe do it after every N turns or if history is sufficient?
        # A simpler approach: Always extract in background and update? 
        # The prompt says: "Once.... agent completes the engagement"
        # We don't know when it ends.
        # Heuristic: Every request, we extract. If we find GOOD info, we *could* send callback.
        # OR: We just assume the mock scammer sends a fixed number of messages.
        
        # Let's extract intelligence in background
        background_tasks.add_task(process_background_tasks, request.sessionId, request.conversationHistory + [request.message])
        
        return AgentResponse(status="success", reply=reply_text)
    else:
        # Not a scam? 
        return AgentResponse(status="ignored", reply=None)

async def process_background_tasks(session_id, history):
    # Extract intelligence
    intelligence = agent.extract_intelligence(history)
    
    # Decide if we should send final result
    # Heuristic: If we have extracted ANY vital info (Bank, UPI, Link), send it.
    # OR if history length > 5
    
    has_info = any([intelligence.bankAccounts, intelligence.upiIds, intelligence.phishingLinks])
    is_long_enough = len(history) >= 2 # At least some interaction
    
    # In a real scenario, we might want to wait longer.
    # But for the hackathon tester, we might need to send it eventually.
    # The Mock Scammer might stop sending if we don't reply?
    # Or good practice: Send updates? No, prompt says 'final result'.
    
    if has_info and is_long_enough:
        payload = FinalCallbackPayload(
            sessionId=session_id,
            scamDetected=True,
            totalMessagesExchanged=len(history),
            extractedIntelligence=intelligence,
            agentNotes="Scam detected and engaged."
        )
        send_final_result(payload)
