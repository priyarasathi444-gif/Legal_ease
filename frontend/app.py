import os
import requests
import streamlit as st
from dotenv import load_dotenv

from backend.utils.document_utils import (
    format_docx,
    format_html_preview,
    format_pdf,
    sanitize_text,
)

load_dotenv()

BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")

st.set_page_config(
    page_title="LegalEase",
    page_icon="⚖️",
    layout="wide",
)

st.markdown(
    """
    <style>
    .main-title {
        text-align:center;
        font-size:42px;
        font-weight:700;
        margin-bottom:0;
    }
    .subtitle {
        text-align:center;
        color:#777;
        margin-bottom:25px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

logo_path = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "assets",
    "logo.png",
)

if os.path.exists(logo_path):
    left, center, right = st.columns([1, 2, 1])
    with center:
        st.image(logo_path, width=180)

st.markdown('<div class="main-title">LegalEase</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">AI-Powered Legal Document Generator</div>',
    unsafe_allow_html=True,
)

st.divider()

col1, col2 = st.columns(2)

with col1:
    document_type = st.text_input(
        "Document Type",
        placeholder="e.g., Freelance Work Contract",
    )

    parties = st.text_area(
        "Parties Involved",
        placeholder="Jane Doe (Service Provider), TechNova Inc. (Client)",
        height=120,
    )

with col2:
    terms = st.text_area(
        "Terms & Conditions",
        placeholder=(
            "Payment within 30 days; Confidentiality must be maintained; "
            "Either party may terminate with 15 days notice"
        ),
        height=120,
        help="Separate each condition using a semicolon (;).",
    )

    dates = st.text_input(
        "Effective Date",
        placeholder="e.g., April 10, 2025",
    )

generate = st.button(
    "Generate Document",
    type="primary",
    use_container_width=True,
)

if generate:
    if not all([document_type.strip(), parties.strip(), terms.strip(), dates.strip()]):
        st.error("Please fill in all required fields.")
    else:
        payload = {
            "document_type": document_type,
            "parties": parties,
            "terms": terms,
            "dates": dates,
        }

        try:
            with st.spinner("Generating your legal document..."):
                response = requests.post(
                    f"{BACKEND_URL}/generate",
                    json=payload,
                    timeout=120,
                )

            if response.ok:
                data = response.json()
                st.session_state["document"] = data["document"]
                st.session_state["doc_type"] = document_type
                st.session_state["terms"] = terms
                st.success("Document generated successfully.")
            else:
                detail = response.json().get("detail", response.text)
                st.error(f"Backend error: {detail}")

        except requests.RequestException as exc:
            st.error(
                "Could not connect to the FastAPI backend. "
                "Make sure the backend is running."
            )
            st.caption(str(exc))

if "document" in st.session_state:
    st.divider()
    st.subheader("Generated Document")

    preview_html = format_html_preview(st.session_state["document"])
    st.markdown(preview_html, unsafe_allow_html=True)

    if st.button("Click to Edit Document", use_container_width=True):
        st.session_state["edit_mode"] = True

    if st.session_state.get("edit_mode", False):
        edited = st.text_area(
            "Edit Document",
            value=st.session_state["document"],
            height=500,
        )
        if st.button("Save Edits", use_container_width=True):
            st.session_state["document"] = edited
            st.session_state["edit_mode"] = False
            st.rerun()

    st.subheader("Download / Save")

    document = sanitize_text(st.session_state["document"])
    doc_type = st.session_state["doc_type"]
    terms_text = st.session_state["terms"]

    txt_data = document.encode("utf-8")
    docx_data = format_docx(document, doc_type, terms_text)
    pdf_data = format_pdf(document, doc_type)

    d1, d2, d3 = st.columns(3)

    with d1:
        st.download_button(
            "Download TXT",
            data=txt_data,
            file_name="LegalEase_Document.txt",
            mime="text/plain",
            use_container_width=True,
        )

    with d2:
        st.download_button(
            "Download DOCX",
            data=docx_data,
            file_name="LegalEase_Document.docx",
            mime=(
                "application/vnd.openxmlformats-officedocument."
                "wordprocessingml.document"
            ),
            use_container_width=True,
        )

    with d3:
        st.download_button(
            "Download PDF",
            data=pdf_data,
            file_name="LegalEase_Document.pdf",
            mime="application/pdf",
            use_container_width=True,
        )

st.divider()
st.caption(
    "LegalEase generates AI-assisted legal content. "
    "Review documents with a qualified legal professional before use."
)
