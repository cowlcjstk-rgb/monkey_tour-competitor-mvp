import streamlit as st
import pandas as pd

from utils.validators import validate_urls
from utils.helpers import generate_run_id
from services.scraper import scrape_product_page
from services.extractor import extract_product_data
from services.analyzer import build_comparison_table, analyze_products
from services.sheets_service import save_run_results

st.set_page_config(page_title="투어 경쟁사 비교 MVP", layout="wide")
st.title("투어상품 경쟁사 비교")

our_url = st.text_input("우리 상품 URL")
comp_a = st.text_input("경쟁사 A URL")
comp_b = st.text_input("경쟁사 B URL")
comp_c = st.text_input("경쟁사 C URL")

category = st.selectbox("카테고리", ["섬투어", "입장권", "스파", "차량", "기타"])

if st.button("비교표 생성"):
    urls = [our_url, comp_a, comp_b, comp_c]
    valid, message = validate_urls(urls)

    if not valid:
        st.error(message)
    else:
        run_id = generate_run_id()
        with st.spinner("분석 중입니다..."):
            raw_pages = [scrape_product_page(url) for url in urls]
            products = [extract_product_data(page, url, category) for page, url in zip(raw_pages, urls)]

            comparison_df = build_comparison_table(products)
            analysis = analyze_products(products)

            save_run_results(run_id, category, urls, comparison_df, analysis)

        st.success("완료되었습니다.")
        st.subheader("비교표")
        st.dataframe(comparison_df, use_container_width=True)

        st.subheader("분석 결과")
        st.write("### 가격 포지션")
        st.write(analysis["positioning"])

        st.write("### 우리 상품 강점")
        for item in analysis["our_strengths"]:
            st.write(f"- {item}")

        st.write("### 우리 상품 약점")
        for item in analysis["our_weaknesses"]:
            st.write(f"- {item}")

        st.write("### 액션 아이템")
        for item in analysis["action_items"]:
            st.write(f"- {item}")
