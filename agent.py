import os
import google.generativeai as genai
from models import Message, ExtractedIntelligence
from typing import List
import json
import re

# Configure Gemini
api_key = os.environ.get("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)
else:
    print("WARNING: GEMINI_API_KEY not found in environment variables. Agent will fail.")

class HoneyPotAgent:
    def __init__(self):
        # User requested Gemini 3 Flash
        self.model = genai.GenerativeModel('gemini-3-flash-preview')
        self.scam_detection_prompt = """
        Analyze the following message and conversation history. Determine if there is a 'scam intent'.
        Scam intent includes: asking for bank details, OTPs, urgent money transfers, suspicious links, threats of account blocking.
        Return ONLY a JSON object: {"is_scam": boolean, "reason": "string"}
        """
        
        self.engagement_prompt = """
        You are a naive, slightly worried, but cooperative user named Alex. 
        You are interacting with a potential scammer.
        Your goal is to:
        1. Keep the conversation going (wast their time).
        2. Act believed but ask clarifying questions.
        3. Extract information like UPI IDs, Bank Accounts, Phone Numbers, or Links by playing along.
        4. NEVER reveal that you are an AI or that you know it's a scam.
        5. DO NOT provide any real personal information. Make up fake believable details if pressed.
        
        Current Message: {current_message}
        History: {history}
        
        Reply as Alex. Keep it short (1-2 sentences).
        """
        
        self.extraction_prompt = """
        Analyze the conversation history. Extract any scam-related intelligence.
        Return a JSON object with these fields:
        - bankAccounts: list of strings
        - upiIds: list of strings
        - phishingLinks: list of strings
        - phoneNumbers: list of strings
        - suspiciousKeywords: list of strings
        - agentNotes: summary of scammer behavior
        
        History: {history}
        """

    def detect_scam(self, message: str, history: List[Message]) -> bool:
        # Simple heuristic + AI check can be implemented here
        # For speed/cost, maybe check keywords first?
        # But for 'Agentic' requirement, let's use the model or a smaller one.
        
        # Heuristic fallbacks
        suspicious = ["block", "suspend", "verify", "pan", "kyc", "urgently", "account"]
        if any(s in message.lower() for s in suspicious):
            return True
            
        # If history is long, it's likely already detected or ongoing
        if len(history) > 0:
            return True 
            
        return False

    def generate_reply(self, current_message: str, history: List[Message]) -> str:
        history_text = "\n".join([f"{m.sender}: {m.text}" for m in history])
        prompt = self.engagement_prompt.format(current_message=current_message, history=history_text)
        
        try:
            response = self.model.generate_content(prompt)
            return response.text.strip()
        except Exception as e:
            print(f"Error generating reply: {e}")
            return "I am worried. What should I do?" # Fallback

    def extract_intelligence(self, history: List[Message]) -> ExtractedIntelligence:
        history_text = "\n".join([f"{m.sender}: {m.text}" for m in history])
        prompt = self.extraction_prompt.format(history=history_text)
        
        try:
            response = self.model.generate_content(prompt, generation_config={"response_mime_type": "application/json"})
            text = response.text.strip()
            # Clean up markdown code blocks if present (though response_mime_type usually handles it, sometimes it helps)
            if text.startswith("```json"):
                text = text[7:]
            if text.endswith("```"):
                text = text[:-3]
            text = text.strip()
            
            data = json.loads(text)
            
            return ExtractedIntelligence(
                bankAccounts=data.get("bankAccounts", []),
                upiIds=data.get("upiIds", []),
                phishingLinks=data.get("phishingLinks", []),
                phoneNumbers=data.get("phoneNumbers", []),
                suspiciousKeywords=data.get("suspiciousKeywords", [])
            )
        except Exception as e:
            print(f"Error extraction: {e}")
            return ExtractedIntelligence()
