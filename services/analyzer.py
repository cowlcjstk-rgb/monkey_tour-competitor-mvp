import pandas as pd
from openai import OpenAI
import json
import streamlit as st

from config.prompts import ANALYSIS_PROMPT

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

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
    prompt = f"{ANALYSIS_PROMPT}\n\n데이터:\n{json.dumps(products, ensure_ascii=False)}"

    response = client.responses.create(
        model="gpt-5-mini",
        input=prompt
    )

    text_output = response.output_text

    try:
        return json.loads(text_output)
    except Exception:
        return {
            "positioning": text_output,
            "our_strengths": [],
            "our_weaknesses": [],
            "action_items": [],
        }
