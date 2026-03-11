import json
from openai import OpenAI
import streamlit as st

from config.prompts import EXTRACTION_PROMPT

def get_openai_client():
    api_key = st.secrets.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY가 Streamlit secrets에 설정되지 않았습니다.")
    return OpenAI(api_key=api_key)

def extract_product_data(page_text: str, url: str, category: str) -> dict:
    client = get_openai_client()

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

    prompt = f"{EXTRACTION_PROMPT}\n\n카테고리: {category}\nURL: {url}\n본문:\n{page_text}"

    response = client.responses.create(
        model="gpt-5-mini",
        input=prompt
    )

    text_output = response.output_text

    try:
        data = json.loads(text_output)
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
