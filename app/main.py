from fastapi import FastAPI, HTTPException, Header, Security, Depends, BackgroundTasks
from app.models import IncomingMessage, APIResponse, ExtractedIntelligence, EngagementMetrics
from app.services.agent import HoneyPotAgent
from app.services.extractor import IntelligenceExtractor
from app.services.reporting import send_final_report
from app.core.config import settings
from typing import Annotated
import logging

# Setup Logger
logging.basicConfig(level=settings.LOG_LEVEL)
logger = logging.getLogger(__name__)

app = FastAPI(title="Agentic Honey-Pot API")

# Initialize Services
agent = HoneyPotAgent()
extractor = IntelligenceExtractor()

# Security Dependency
async def verify_api_key(x_api_key: Annotated[str, Header()]):
    # Allow any key for now or match specific one
    if not x_api_key:
        raise HTTPException(status_code=403, detail="X-API-KEY header missing")
    return x_api_key

@app.post("/chat", response_model=APIResponse)
@app.post("/api/v1/chat", response_model=APIResponse)
async def chat_endpoint(
    request: IncomingMessage, 
    background_tasks: BackgroundTasks,
    api_key: str = Security(verify_api_key)
):
    logger.info(f"Received message for session {request.sessionId}")
    
    # 1. Scam Detection
    is_scam = await agent.detect_scam(request.message.text)
    
    # 2. Extract Intelligence
    current_intelligence = ExtractedIntelligence() 
    
    full_text = request.message.text
    for msg in request.conversationHistory:
        full_text += " " + msg.text
        
    extracted = extractor.extract(full_text, current_intelligence)
    
    # 3. LLM Enhanced Extraction
    llm_extracted = await agent.extract_smart_intelligence(request.message.text)
    if "bankAccounts" in llm_extracted:
        extracted.bankAccounts.extend(llm_extracted["bankAccounts"])
        # Dedupe
        extracted.bankAccounts = list(set(extracted.bankAccounts))

    # 4. Agent Response
    if is_scam:
        # Generate Agent Reply
        reply_text = await agent.generate_response(request.message.text, request.conversationHistory)
        agent_notes = "Scam detected. Engaged with naive persona."
    else:
        reply_text = "Hello, I am not sure what you mean. Please clarify."
        agent_notes = "No scam detected yet."

    # 5. Metrics
    total_messages = len(request.conversationHistory) + 1
    
    # 6. Periodic Reporting (Triggered if scam is detected)
    # We send an update if scam is detected. The endpoint is "update...", so multiple calls might be okay.
    # To be safe and ensure we capture late-stage intelligence, we send it on every turn after detection.
    if is_scam:
        background_tasks.add_task(
            send_final_report,
            session_id=request.sessionId,
            scam_detected=is_scam,
            total_messages=total_messages,
            intelligence=extracted,
            agent_notes=agent_notes
        )
    
    return APIResponse(
        status="success",
        scamDetected=is_scam,
        engagementMetrics=EngagementMetrics(
            totalMessagesExchanged=total_messages,
            engagementDurationSeconds=total_messages * 15 # Mock estimate
        ),
        extractedIntelligence=extracted,
        agentNotes=agent_notes
    )

@app.get("/")
def health_check():
    return {"status": "ok", "service": "Agentic Honey-Pot"}
