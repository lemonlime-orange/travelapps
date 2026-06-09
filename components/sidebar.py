"""
sidebar.py
사이드바 필터 및 네비게이션 컴포넌트
"""

import streamlit as st


def render_sidebar(categories: list) -> dict:
    """
    사이드바를 렌더링하고 사용자 선택값을 반환합니다.
    반환값: {"category": str, "search": str}
    """
    with st.sidebar:
        st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/0/09/Flag_of_South_Korea.svg/320px-Flag_of_South_Korea.svg.png", width=80)
        st.title("🇰🇷 Korea Travel Apps")
        st.caption("Your digital guide to South Korea")
        st.divider()

        # 검색창
        search_query = st.text_input(
            "🔍 Search apps",
            placeholder="e.g. food, taxi, map..."
        )

        # 카테고리 필터
        st.markdown("**📂 Filter by Category**")
        all_categories = ["All"] + categories
        selected_category = st.selectbox(
            "Category",
            options=all_categories,
            label_visibility="collapsed"
        )

        st.divider()
        st.caption("📌 App data stored in Supabase")
        st.caption("Built with Streamlit 🎈")

    return {
        "category": selected_category,
        "search": search_query,
    }
