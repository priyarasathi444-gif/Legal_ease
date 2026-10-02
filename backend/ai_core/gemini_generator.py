import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()


class GeminiDocumentGenerator:
    """Creates structured legal documents using Google Gemini."""

    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.model_name = os.getenv("GEMINI_MODEL", "gemini-1.5-pro")

        if not self.api_key:
            raise ValueError(
                "GEMINI_API_KEY is missing. Add it to your .env file."
            )

        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel(self.model_name)

    def build_prompt(self, document_type, parties, terms, dates):
        return f"""
You are LegalEase, an AI-powered legal document drafting assistant.

Create a professional, structured legal document based on the information below.

Document Type:
{document_type}

Parties Involved:
{parties}

Terms and Conditions:
{terms}

Effective Date:
{dates}

Requirements:
1. Use a formal legal-document style.
2. Include a clear title.
3. Identify the parties.
4. Include the effective date.
5. Convert the supplied terms into numbered or clearly separated clauses.
6. Add appropriate standard sections where relevant, such as:
   - Definitions
   - Scope / Responsibilities
   - Payment or Consideration, if applicable
   - Confidentiality, if applicable
   - Term and Termination
   - Governing Law
   - Signatures
7. Do not invent specific personal, financial, statutory or jurisdictional facts.
8. Keep the supplied facts unchanged.
9. Make the output easy to edit and export.
10. End with signature placeholders when appropriate.

Return only the document text, without Markdown code fences.
"""

    def generate_document(self, document_type, parties, terms, dates):
        prompt = self.build_prompt(document_type, parties, terms, dates)
        response = self.model.generate_content(prompt)

        if not response or not response.text:
            raise RuntimeError("Gemini returned an empty response.")

        return response.text.strip()
