from pydantic import BaseModel, Field
from typing import List, Optional, Any
from datetime import datetime

class Message(BaseModel):
    sender: str
    text: str
    timestamp: datetime | str  # Allow str for flexibility, but ideally datetime

class IncomingMessage(BaseModel):
    sessionId: str
    message: Message
    conversationHistory: List[Message] = []
    metadata: Optional[dict] = {}

class EngagementMetrics(BaseModel):
    engagementDurationSeconds: int = 0
    totalMessagesExchanged: int = 0

class ExtractedIntelligence(BaseModel):
    bankAccounts: List[str] = []
    upiIds: List[str] = []
    phishingLinks: List[str] = []
    phoneNumbers: List[str] = []
    suspiciousKeywords: List[str] = []

class APIResponse(BaseModel):
    status: str
    scamDetected: bool
    engagementMetrics: EngagementMetrics
    extractedIntelligence: ExtractedIntelligence
    agentNotes: str = ""
