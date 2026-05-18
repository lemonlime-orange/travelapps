"""
app_card.py
앱 정보를 카드 형식으로 표시하는 UI 컴포넌트
"""

import streamlit as st


def render_app_card(app: dict):
    """
    앱 1개를 카드 형태로 렌더링합니다.
    app: CSV 한 행을 dict로 변환한 데이터
    """
    features = app["features"].split("|")
    
    with st.container(border=True):
        # 앱 헤더 (아이콘 + 이름 + 카테고리)
        col1, col2 = st.columns([1, 5])
        with col1:
            st.markdown(f"<div style='font-size:2.5rem; text-align:center'>{app['icon']}</div>", unsafe_allow_html=True)
        with col2:
            st.markdown(f"### {app['name']}")
            st.caption(f"📂 {app['category']}  •  📱 {app['platform']}  •  ⭐ {app['rating']}")

        # 앱 설명
        st.markdown(app["description"])

        # 주요 기능 목록
        st.markdown("**✅ Key Features**")
        cols = st.columns(2)
        for i, feature in enumerate(features):
            cols[i % 2].markdown(f"- {feature.strip()}")

        # 여행 팁
        st.info(f"💡 **Tip:** {app['tips']}")

        # 다운로드 링크
        st.markdown(f"[🔗 Visit Official Site]({app['download_url']})")
