"""
situation_helper.py
상황 도우미 UI 렌더러 — 카테고리 선택 후 상황 표시
"""

import streamlit as st
import pandas as pd
from components.data_loader import load_situations_by_category, get_situation_categories, load_apps, get_apps_by_ids


def render_situation_helper():
    """상황 도우미 UI를 렌더링합니다."""
    
    st.subheader("🎯 What's Your Situation?")
    st.markdown("Select a category to find the right app for your needs.")
    
    # 카테고리 버튼
    categories = get_situation_categories()
    
    # 세션 상태 초기화
    if "selected_situation_category" not in st.session_state:
        st.session_state.selected_situation_category = None
    
    st.write("**Categories:**")
    cols = st.columns(2)
    for i, category in enumerate(categories):
        with cols[i % 2]:
            if st.button(f"📁 {category}", key=f"cat_{category}", use_container_width=True):
                st.session_state.selected_situation_category = category
                st.rerun()
    
    st.divider()
    
    # 선택된 카테고리의 상황들 표시
    if st.session_state.selected_situation_category:
        category = st.session_state.selected_situation_category
        situations_df = load_situations_by_category(category)
        
        st.subheader(f"📋 {category}")
        
        if situations_df.empty:
            st.info(f"No situations found in this category.")
        else:
            for _, row in situations_df.iterrows():
                with st.expander(f"{row['emoji']} {row['situation']}", expanded=False):
                    st.markdown(f"_{row['description']}_")
                    
                    # 관련 앱 표시
                    if pd.notna(row['app_ids']) and str(row['app_ids']).strip():
                        app_ids = [int(x.strip()) for x in str(row['app_ids']).split(",") if x.strip()]
                        df_apps = load_apps()
                        related_apps = get_apps_by_ids(df_apps, app_ids)
                        
                        if not related_apps.empty:
                            st.write("**Recommended Apps:**")
                            for _, app in related_apps.iterrows():
                                st.caption(f"🔹 {app['name']} — {app['description']}")
        
        st.divider()
        if st.button("← Back to Categories"):
            st.session_state.selected_situation_category = None
            st.rerun()
