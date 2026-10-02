# LegalEase: AI-Powered Legal Document Generator

LegalEase generates customizable legal documents using Google Gemini through a FastAPI backend and Streamlit frontend.

## Features
- Generate contracts, agreements, NDAs, lease agreements, employment letters, etc.
- Inputs: document type, parties, terms and effective date
- Gemini-powered document generation
- Editable preview
- Download as TXT, DOCX and PDF
- DOCX/PDF branding with logo and footer
- Terms table in DOCX
- Dark HTML preview

## Architecture
Streamlit Frontend -> FastAPI Backend -> Gemini AI Core
                                  -> Document Formatting Utilities

## Setup

### 1. Create virtual environment
```bash
python -m venv venv
```

Windows:
```bash
venv\Scripts\activate
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Gemini API key
Copy `.env.example` to `.env` and add your Gemini API key:
```env
GEMINI_API_KEY=your_api_key_here
```

### 4. Start FastAPI
From the project root:
```bash
uvicorn backend.main:app --reload
```

Backend:
http://127.0.0.1:8000

### 5. Start Streamlit
Open another terminal:
```bash
streamlit run frontend/app.py
```

Frontend:
http://localhost:8501

## Important
This project generates legal information/documents and is not a substitute for advice from a qualified lawyer. Review generated documents before use.
