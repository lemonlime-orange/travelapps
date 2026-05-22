"""
app_card.py
앱 카드 UI 컴포넌트 — 즐겨찾기 토글 포함
"""

import streamlit as st
from components.data_loader import is_favorite, toggle_favorite


def render_app_card(app: dict, show_favorite: bool = True):
    """
    앱 1개를 카드 형태로 렌더링합니다.
    show_favorite: 즐겨찾기 버튼 표시 여부
    """
    features = [f.strip() for f in app["features"].split("|")]
    app_id = int(app["id"])
    fav = is_favorite(app_id)

    with st.container(border=True):
        # 헤더: 이미지 or 아이콘 + 이름 + 다운로드 버튼 + 즐겨찾기 버튼
        col_icon, col_title, col_download, col_fav = st.columns([1, 5, 1, 1])
        with col_icon:
            image_url = str(app.get("image_url", "") or "").strip()
            if image_url:
                st.image(image_url, width=100, clamp=True)
            else:
                st.markdown(
                    f"<div style='font-size:2.2rem; text-align:center; padding-top:4px'>{app.get('icon', '')}</div>",
                    unsafe_allow_html=True,
                )
        with col_title:
            st.markdown(f"### {app['name']}")
            st.caption(f"📂 {app['category']}  •  📱 {app['platform']}  •  ⭐ {app['rating']}")
        # 다운로드 버튼 (즐겨찾기 버튼 왼쪽)
        download_url = str(app.get("download_url", "") or "").strip()
        with col_download:
            if download_url:
                btn_html = (
                    f"<a href=\"{download_url}\" target=\"_blank\" "
                    "style=\"background-color:#1f77ff;color:white;padding:8px 12px;"
                    "border-radius:6px;text-decoration:none;display:inline-block;font-weight:600;"
                    "font-size:0.95rem\">Download</a>"
                )
                st.markdown(btn_html, unsafe_allow_html=True)
            else:
                st.markdown("<div style='color:#888; font-size:0.9rem'>No link</div>", unsafe_allow_html=True)

        if show_favorite:
            with col_fav:
                star = "⭐" if fav else "☆"
                if st.button(star, key=f"fav_{app_id}", help="Add to Favorites"):
                    toggle_favorite(app_id)
                    st.rerun()

        # 설명
        st.markdown(app["description"])

        # 주요 기능
        st.markdown("**✅ Key Features**")
        cols = st.columns(2)
        for i, feature in enumerate(features):
            cols[i % 2].markdown(f"- {feature}")

        # 여행 팁
        st.info(f"💡 **Tip:** {app['tips']}")

        # 링크는 상단의 Download 버튼으로 대체됨
