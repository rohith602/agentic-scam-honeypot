import google.generativeai as genai
from app.core.config import settings
from app.models import IncomingMessage, ExtractedIntelligence
import json

genai.configure(api_key=settings.GEMINI_API_KEY)

class HoneyPotAgent:
    def __init__(self):
        # Use verified working model
        self.model = genai.GenerativeModel('models/gemini-2.5-flash')
        self.scam_detection_model = genai.GenerativeModel('models/gemini-2.5-flash')

    async def generate_response(self, text: str, history: list) -> str:
        # Construct prompt related to the persona
        # Persona: Naive, slightly elderly person who is worried but technically inept.
        system_prompt = (
            "You are a 65-year-old retired school teacher named Lakshmi. "
            "You are not tech-savvy. You received a message that worries you. "
            "You want to resolve the issue but you are slow to understand technical terms. "
            "You ask clarifying questions. You NEVER reveal you are an AI. "
            "Keep your responses short, under 30 words, like an SMS user. "
            "If they ask for money or details, act confused or ask why it's needed."
        )
        
        formatted_history = []
        for msg in history:
            role = "user" if msg.sender == "scammer" else "model"
            formatted_history.append({"role": role, "parts": [msg.text]})
        
        # Add current message
        formatted_history.append({"role": "user", "parts": [text]})

        try:
            # We can't easily inject system prompt into chat history without specific API structure
            # easier to just concat for single turn or use chat session if persistent.
            # For this API, it's stateless per request, but we have history.
            # We'll use start_chat with history.
            chat = self.model.start_chat(history=formatted_history[:-1])
            response = chat.send_message(text)
            return response.text
        except Exception as e:
            print(f"LLM GENERATION ERROR: {e}")
            # Fallback if history structure fails or API error
            full_prompt = f"{system_prompt}\n\nThe conversation so far:\n{history}\n\nScammer says: {text}\n\nLakshmi:"
            try:
                response = self.model.generate_content(full_prompt)
                return response.text
            except Exception as e2:
                print(f"LLM FALLBACK ERROR: {e2}")
                # Ultimate fallback
                return "Oh dear, I am confused. My internet is acting up. What did you say?"

    async def detect_scam(self, text: str) -> bool:
        prompt = (
            f"Analyze this message for scam intent: '{text}'. "
            "Respond ONLY with 'TRUE' if it is a scam (phishing, financial fraud, urgency) "
            "or 'FALSE' if it is safe."
        )
        try:
            response = self.model.generate_content(prompt)
            return "TRUE" in response.text.upper()
        except:
            # Fallback heuristic: keyword based
            keywords = ["block", "suspend", "verify", "pan", "kyc", "urgent", "credit card", "bank", "expire"]
            if any(k in text.lower() for k in keywords):
                return True
            return False

    async def extract_smart_intelligence(self, text: str) -> dict:
        # Use LLM to extract bank accounts or subtle info
        prompt = (
            f"Extract bank account numbers, IFSC codes, or specific monetary amounts requested from this text: '{text}'. "
            "Return JSON format: {{'bankAccounts': [], 'amounts': []}}. Return empty lists if none found."
        )
        try:
            response = self.model.generate_content(prompt, generation_config={"response_mime_type": "application/json"})
            return json.loads(response.text)
        except:
            return {}
