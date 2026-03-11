import json
import streamlit as st
from google import genai
from google.genai import types

from config.prompts import EXTRACTION_PROMPT

EXTRACTION_SCHEMA = {
    "type": "object",
    "properties": {
        "source_name": {"type": ["string", "null"]},
        "product_name": {"type": ["string", "null"]},
        "price": {"type": ["number", "null"]},
        "currency": {"type": ["string", "null"]},
        "tour_type": {"type": ["string", "null"]},
        "duration": {"type": ["string", "null"]},
        "pickup": {"type": ["string", "null"]},
        "included": {"type": "array", "items": {"type": "string"}},
        "excluded": {"type": "array", "items": {"type": "string"}},
        "highlights": {"type": "array", "items": {"type": "string"}},
        "child_policy": {"type": ["string", "null"]},
        "cancellation_policy": {"type": ["string", "null"]},
        "options": {"type": "array", "items": {"type": "string"}},
        "summary_strength": {"type": ["string", "null"]},
        "summary_weakness": {"type": ["string", "null"]},
    },
    "required": [
        "source_name",
        "product_name",
        "price",
        "currency",
        "tour_type",
        "duration",
        "pickup",
        "included",
        "excluded",
        "highlights",
        "child_policy",
        "cancellation_policy",
        "options",
        "summary_strength",
        "summary_weakness",
    ],
}

def get_gemini_client():
    api_key = st.secrets.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY가 Streamlit secrets에 설정되지 않았습니다.")
    return genai.Client(api_key=api_key)

def extract_product_data(page_text: str, url: str, category: str) -> dict:
    if page_text.startswith("SCRAPE_ERROR:"):
        return {
            "source_name": url,
            "url": url,
            "product_name": None,
            "price": None,
            "currency": None,
            "tour_type": None,
            "duration": None,
            "pickup": "unknown",
            "included": [],
            "excluded": [],
            "highlights": [],
            "child_policy": None,
            "cancellation_policy": None,
            "options": [],
            "summary_strength": None,
            "summary_weakness": None,
            "warning": page_text,
        }

    client = get_gemini_client()

    prompt = f"""
{EXTRACTION_PROMPT}

카테고리: {category}
URL: {url}

본문:
{page_text}
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_json_schema=EXTRACTION_SCHEMA,
        ),
    )

    try:
        data = json.loads(response.text)
        data["url"] = url
        return data
    except Exception:
        return {
            "source_name": url,
            "url": url,
            "product_name": None,
            "price": None,
            "currency": None,
            "tour_type": None,
            "duration": None,
            "pickup": "unknown",
            "included": [],
            "excluded": [],
            "highlights": [],
            "child_policy": None,
            "cancellation_policy": None,
            "options": [],
            "summary_strength": None,
            "summary_weakness": None,
            "warning": "AI_PARSE_ERROR",
        }
