"""
app.py
🇰🇷 Korea Travel Apps Guide — 메인 진입점

실행 방법:
    streamlit run app.py
"""

import streamlit as st
import sys
import os

# components 폴더를 import 경로에 추가
sys.path.append(os.path.join(os.path.dirname(__file__), "components"))

from data_loader import load_apps, get_categories, filter_by_category, search_apps
from app_card import render_app_card
from sidebar import render_sidebar

# ── 페이지 기본 설정 ──────────────────────────────────────────
st.set_page_config(
    page_title="Korea Travel Apps",
    page_icon="🇰🇷",
    layout="wide",
)

# ── 데이터 로드 ───────────────────────────────────────────────
df = load_apps()
categories = get_categories(df)

# ── 사이드바 렌더링 & 필터 값 가져오기 ────────────────────────
filters = render_sidebar(categories)

# ── 필터 적용 ─────────────────────────────────────────────────
filtered_df = filter_by_category(df, filters["category"])
filtered_df = search_apps(filtered_df, filters["search"])

# ── 메인 헤더 ─────────────────────────────────────────────────
st.title("🇰🇷 Essential Apps for Traveling in South Korea")
st.markdown(
    "Discover the best apps locals use every day — "
    "from navigation and food delivery to translation and transport."
)
st.divider()

# ── 결과 요약 ─────────────────────────────────────────────────
col_info, col_spacer = st.columns([3, 1])
with col_info:
    total = len(filtered_df)
    label = filters["category"] if filters["category"] != "All" else "all categories"
    st.caption(f"Showing **{total} app{'s' if total != 1 else ''}** in {label}")

# ── 앱 카드 목록 ──────────────────────────────────────────────
if filtered_df.empty:
    st.warning("😕 No apps found. Try a different search or category.")
else:
    for _, row in filtered_df.iterrows():
        render_app_card(row.to_dict())
        st.write("")  # 카드 사이 여백
