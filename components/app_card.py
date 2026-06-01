"""
app_card.py
앱 카드 UI 컴포넌트 — 즐겨찾기 토글 포함
"""

import streamlit as st
from components.data_loader import is_favorite, toggle_favorite, is_downloaded, toggle_downloaded


def render_app_card(app: dict, show_favorite: bool = True, show_download_toggle: bool = True, show_download_remove: bool = False):
    """
    앱 1개를 카드 형태로 렌더링합니다.
    show_favorite: 즐겨찾기 버튼 표시 여부
    """
    features = [f.strip() for f in app["features"].split("|")]
    app_id = int(app["id"])
    fav = is_favorite(app_id)

    with st.container(border=True):
        # 헤더: 이미지 or 아이콘 + 이름 + 다운로드 링크 + 다운로드 표시 버튼 + 즐겨찾기 버튼
        col_icon, col_title, col_download_link, col_download_mark, col_fav = st.columns([1, 5, 1, 1, 1])
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
        # 다운로드 링크
        download_url = str(app.get("download_url", "") or "").strip()
        with col_download_link:
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

        # 다운로드 표시(사용자가 이미 다운받았는지 토글하는 버튼)
        dl = is_downloaded(app_id)
        if show_download_toggle:
            with col_download_mark:
                mark = "📥" if dl else "⬇️"
                if st.button(mark, key=f"dl_{app_id}", help="Mark as Downloaded"):
                    toggle_downloaded(app_id)
                    st.rerun()

        if show_favorite:
            with col_fav:
                star = "⭐" if fav else "☆"
                if st.button(star, key=f"fav_{app_id}", help="Add to Favorites"):
                    toggle_favorite(app_id)
                    st.rerun()

        # 설명
        st.markdown(app["description"])

        # 사용 방법(가이드) 이미지가 있으면 표시 (각 이미지 아래에 캡션 표시)
        guide_images = [s for s in str(app.get("guide_images", "") or "").split("|") if s.strip()]
        guide_captions = [s for s in str(app.get("guide_image_captions", "") or "").split("|") if s.strip()]
        if guide_images:
            st.markdown("**📖 Usage Guide (images)**")
            cols = st.columns(min(3, len(guide_images)))
            for i, img in enumerate(guide_images):
                try:
                    cols[i % 3].image(img, width=240)
                except Exception:
                    cols[i % 3].markdown(f"Failed to load: {img}")
                # 캡션 표시 (있을 경우, 검정색 #000000)
                caption = guide_captions[i] if i < len(guide_captions) else ""
                if caption:
                    cols[i % 3].markdown(f"<div style=\"color:#000000; font-size:0.9rem; margin-top:6px\">{caption}</div>", unsafe_allow_html=True)

        # 주요 기능
        st.markdown("**✅ Key Features**")
        cols = st.columns(2)
        for i, feature in enumerate(features):
            cols[i % 2].markdown(f"- {feature}")

        # 여행 팁
        st.info(f"💡 **Tip:** {app['tips']}")

        # 링크는 상단의 Download 버튼으로 대체됨

        # 다운로드 페이지에서 항목 제거 버튼
        if show_download_remove:
            if st.button("Remove from Downloads", key=f"remove_{app_id}"):
                toggle_downloaded(app_id)
                st.rerun()
