import re
from app.models import ExtractedIntelligence

class IntelligenceExtractor:
    def extract(self, text: str, existing: ExtractedIntelligence) -> ExtractedIntelligence:
        # Regex patterns
        upi_pattern = r"[\w\.-]+@[\w]+"
        url_pattern = r"https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+"
        phone_pattern = r"(?:\+91[\-\s]?)?[6-9]\d{9}"
        # Bank account is harder with just regex, usually 9-18 digits. 
        # But we need to be careful not to match timestamps or other numbers.
        # Let's try to match "Account ... XXXXX" context or just long digits if context exists.
        # For this hackathon, we can use a simpler heuristic or just LLM later. 
        # Let's stick to Regex for high confidence fields.
        
        upis = re.findall(upi_pattern, text)
        links = re.findall(url_pattern, text)
        phones = re.findall(phone_pattern, text)
        
        # Simple keyword detection for 'suspiciousKeywords'
        keywords = ["urgent", "verify", "block", "suspend", "kyc", "pan", "aadhar", "apk"]
        found_keywords = [k for k in keywords if k in text.lower()]

        # Merge with existing (using set to avoid duplicates)
        new_intelligence = ExtractedIntelligence(
            upiIds=list(set(existing.upiIds + upis)),
            phishingLinks=list(set(existing.phishingLinks + links)),
            phoneNumbers=list(set(existing.phoneNumbers + phones)),
            suspiciousKeywords=list(set(existing.suspiciousKeywords + found_keywords)),
            bankAccounts=existing.bankAccounts # Keep existing, maybe LLM adds this
        )
        return new_intelligence
