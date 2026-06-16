"""
app_card.py
앱 카드 UI 컴포넌트 — 즐겨찾기 토글 포함
"""

import streamlit as st
from components.data_loader import is_favorite, toggle_favorite, is_downloaded, toggle_downloaded


GUIDE_BUTTON_STYLE = """
<style>
div[data-testid="stButton"] button[kind="primary"] {
    background-color: #1f77ff;
    border-color: #1f77ff;
    color: #ffffff;
}
div[data-testid="stButton"] button[kind="primary"]:hover {
    background-color: #155ed1;
    border-color: #155ed1;
    color: #ffffff;
}
div[data-testid="stButton"] button[kind="primary"]:focus {
    box-shadow: 0 0 0 0.2rem rgba(31, 119, 255, 0.25);
}
</style>
"""


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
        guide_images = [s.strip() for s in str(app.get("guide_images", "") or "").split("|") if s.strip()]
        guide_captions = [s.strip() for s in str(app.get("guide_image_captions", "") or "").split("|")]
        if guide_images:
            is_open_key = f"guide_open_{app_id}"
            index_key = f"guide_index_{app_id}"

            if is_open_key not in st.session_state:
                st.session_state[is_open_key] = False
            if index_key not in st.session_state:
                st.session_state[index_key] = 0

            button_label = "Hide How To Use" if st.session_state[is_open_key] else "How To Use"
            st.markdown(GUIDE_BUTTON_STYLE, unsafe_allow_html=True)
            if st.button(button_label, key=f"guide_toggle_{app_id}", type="primary"):
                st.session_state[is_open_key] = not st.session_state[is_open_key]
                st.rerun()

            if st.session_state[is_open_key]:
                current_index = st.session_state[index_key] % len(guide_images)
                current_image = guide_images[current_index]
                current_caption = guide_captions[current_index] if current_index < len(guide_captions) else ""

                st.markdown("**How To Use**")
                prev_col, image_col, next_col = st.columns([1, 6, 1])

                with prev_col:
                    st.write("")
                    st.write("")
                    if st.button("<", key=f"guide_prev_{app_id}", disabled=len(guide_images) <= 1, help="Previous guide image"):
                        st.session_state[index_key] = (current_index - 1) % len(guide_images)
                        st.rerun()

                with image_col:
                    try:
                        st.image(current_image, use_container_width=True)
                    except Exception:
                        st.warning(f"Failed to load guide image: {current_image}")
                    if current_caption:
                        st.caption(current_caption)
                    st.caption(f"{current_index + 1} / {len(guide_images)}")

                with next_col:
                    st.write("")
                    st.write("")
                    if st.button(">", key=f"guide_next_{app_id}", disabled=len(guide_images) <= 1, help="Next guide image"):
                        st.session_state[index_key] = (current_index + 1) % len(guide_images)
                        st.rerun()
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
