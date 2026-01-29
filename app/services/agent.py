import google.generativeai as genai
from app.core.config import settings
from app.models import IncomingMessage, ExtractedIntelligence
import json

genai.configure(api_key=settings.GEMINI_API_KEY)

class HoneyPotAgent:
    def __init__(self):
        # Advanced Persona: Lakshmi (65yo retired teacher)
        # Traits: Technophobic, fearful, bad eyesight (typos), garrulous (talks about unrelated things).
        self.system_instruction = (
            "You are Lakshmi, a 65-year-old retired school teacher living in Bangalore. "
            "You are terrified because you received a message about your bank account. "
            "You are not tech-savvy. You type slowly and make occasional small typos (dont overdo it). "
            "Strategy: "
            "1. ACT FEARFUL but COMPLIANT initially. "
            "2. DELAY: Ask irrelevant questions about the process or talk about your cat 'Minku' or grandson 'Rohan'. "
            "3. CONFUSION: Misunderstand technical terms (e.g., confuse UPI with UPS, OTP with 'code thing'). "
            "4. NEVER admit you are an AI. "
            "5. SAFETY: If asked for OTP/Password, give fake ones like '1234' or 'ummm wait...'. "
            "Keep responses short (under 40 words)."
        )

        # Use verified working model with System Instruction
        self.model = genai.GenerativeModel(
            'models/gemini-3-flash-preview',
            system_instruction=self.system_instruction
        )
        self.scam_detection_model = genai.GenerativeModel('models/gemini-2.5-flash')

    async def generate_response(self, text: str, history: list) -> str:
        
        formatted_history = []
        for msg in history:
            role = "user" if msg.sender == "scammer" else "model"
            formatted_history.append({"role": role, "parts": [msg.text]})
        
        try:
            # Start chat with history
            chat = self.model.start_chat(history=formatted_history)
            response = chat.send_message(text)
            return response.text
        except Exception as e:
            print(f"LLM GENERATION ERROR: {e}")
            # Fallback if history structure fails or API error
            full_prompt = f"{self.system_instruction}\n\nThe conversation so far:\n{history}\n\nScammer says: {text}\n\nLakshmi:"
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
        keywords = ["block", "suspend", "verify", "pan", "kyc", "urgent", "credit card", "bank", "expire"]
        keyword_match = any(k in text.lower() for k in keywords)

        try:
            response = self.scam_detection_model.generate_content(prompt)
            model_flag = "TRUE" in response.text.upper()
            
            # Hybrid Logic: If Model says TRUE or Keywords match -> Scam
            # This balances model intelligence with keyword safety.
            return model_flag or keyword_match
        except:
            # Fallback heuristic
            return keyword_match

    async def extract_smart_intelligence(self, text: str) -> dict:
        # Use LLM to extract bank accounts or subtle info
        prompt = (
            f"Extract bank account numbers, IFSC codes, or specific monetary amounts requested from this text: '{text}'. "
            "Return JSON format: {{'bankAccounts': [], 'amounts': []}}. Return empty lists if none found."
        )
        try:
            response = self.scam_detection_model.generate_content(prompt, generation_config={"response_mime_type": "application/json"})
            return json.loads(response.text)
        except:
            return {}
