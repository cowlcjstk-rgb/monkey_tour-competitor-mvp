import gspread
import streamlit as st
from datetime import datetime

def get_gspread_client():
    creds = st.secrets["GOOGLE_SERVICE_ACCOUNT_JSON"]
    return gspread.service_account_from_dict(dict(creds))

def save_run_results(run_id: str, category: str, urls: list[str], comparison_df, analysis: dict):
    client = get_gspread_client()
    sheet = client.open(st.secrets["GOOGLE_SHEET_NAME"])

    input_ws = sheet.worksheet("input_history")
    analysis_ws = sheet.worksheet("analysis_results")
    compare_ws = sheet.worksheet("comparison_results")

    input_ws.append_row([
        run_id,
        datetime.now().isoformat(),
        category,
        urls[0],
        urls[1],
        urls[2],
        urls[3],
    ])

    for _, row in comparison_df.iterrows():
        compare_ws.append_row([
            run_id,
            row["항목"],
            row["우리 상품"],
            row["경쟁사 A"],
            row["경쟁사 B"],
            row["경쟁사 C"],
        ])

    analysis_ws.append_row([
        run_id,
        analysis.get("positioning", ""),
        " | ".join(analysis.get("our_strengths", [])),
        " | ".join(analysis.get("our_weaknesses", [])),
        " | ".join(analysis.get("action_items", [])),
    ])
