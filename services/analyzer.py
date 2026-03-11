import json
import pandas as pd
import streamlit as st
from google import genai
from google.genai import types

from config.prompts import ANALYSIS_PROMPT

ANALYSIS_SCHEMA = {
    "type": "object",
    "properties": {
        "positioning": {"type": "string"},
        "our_strengths": {"type": "array", "items": {"type": "string"}},
        "our_weaknesses": {"type": "array", "items": {"type": "string"}},
        "action_items": {"type": "array", "items": {"type": "string"}},
    },
    "required": ["positioning", "our_strengths", "our_weaknesses", "action_items"],
}

def get_gemini_client():
    api_key = st.secrets.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY가 Streamlit secrets에 설정되지 않았습니다.")
    return genai.Client(api_key=api_key)

def build_comparison_table(products: list[dict]) -> pd.DataFrame:
    labels = [
        ("상품명", "product_name"),
        ("가격", "price"),
        ("통화", "currency"),
        ("투어 유형", "tour_type"),
        ("소요시간", "duration"),
        ("픽업 여부", "pickup"),
        ("포함사항", "included"),
        ("불포함사항", "excluded"),
        ("주요 구성", "highlights"),
        ("아동 규정", "child_policy"),
        ("취소 규정", "cancellation_policy"),
        ("옵션 수", "options"),
        ("한줄 강점", "summary_strength"),
        ("한줄 약점", "summary_weakness"),
    ]

    rows = []
    names = ["우리 상품", "경쟁사 A", "경쟁사 B", "경쟁사 C"]

    for label, key in labels:
        row = {"항목": label}
        for name, product in zip(names, products):
            value = product.get(key)
            if isinstance(value, list):
                if key == "options":
                    value = len(value)
                else:
                    value = ", ".join(value)
            row[name] = value
        rows.append(row)

    return pd.DataFrame(rows)

def analyze_products(products: list[dict]) -> dict:
    client = get_gemini_client()

    prompt = f"""
{ANALYSIS_PROMPT}

데이터:
{json.dumps(products, ensure_ascii=False)}
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_json_schema=ANALYSIS_SCHEMA,
        ),
    )

    try:
        return json.loads(response.text)
    except Exception:
        return {
            "positioning": response.text,
            "our_strengths": [],
            "our_weaknesses": [],
            "action_items": [],
        }
