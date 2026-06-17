"""
app_card.py
앱 카드 UI 컴포넌트 — 즐겨찾기 토글 포함
"""

from html import escape

import streamlit as st
from components.data_loader import is_favorite, toggle_favorite, is_downloaded, toggle_downloaded


DOWNLOAD_LINK_STYLE = (
    "background-color:#1f77ff;color:white;padding:8px 12px;"
    "border-radius:6px;text-decoration:none;display:block;font-weight:600;"
    "font-size:0.88rem;line-height:1;white-space:nowrap;min-width:118px;"
    "text-align:center;box-sizing:border-box"
)


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


def _split_image_list(value):
    return [s.strip() for s in str(value or "").split("|") if s.strip()]


def _split_caption_list(value):
    return [s.strip() for s in str(value or "").split("|")]


def _render_image_gallery_button(app_id, title, key_prefix):
    active_key = f"gallery_active_{app_id}"
    index_key = f"{key_prefix}_index_{app_id}"

    if active_key not in st.session_state:
        st.session_state[active_key] = ""
    if index_key not in st.session_state:
        st.session_state[index_key] = 0

    is_open = st.session_state[active_key] == key_prefix
    button_label = f"Hide {title}" if is_open else title
    if st.button(button_label, key=f"{key_prefix}_toggle_{app_id}", type="primary"):
        st.session_state[active_key] = "" if is_open else key_prefix
        st.session_state[index_key] = 0
        st.rerun()

    return st.session_state[active_key] == key_prefix


def _render_image_gallery_content(app_id, title, images, captions, key_prefix):
    index_key = f"{key_prefix}_index_{app_id}"

    if not images:
        return

    current_index = st.session_state[index_key] % len(images)
    current_image = images[current_index]
    current_caption = captions[current_index] if current_index < len(captions) else ""

    st.markdown(f"**{title}**")
    prev_col, image_col, next_col = st.columns([1, 6, 1])

    with prev_col:
        st.write("")
        st.write("")
        if st.button("←", key=f"{key_prefix}_prev_{app_id}", disabled=len(images) <= 1, help=f"Previous {title} image"):
            st.session_state[index_key] = (current_index - 1) % len(images)
            st.rerun()

    with image_col:
        try:
            st.image(current_image, use_container_width=True)
        except Exception:
            st.warning(f"Failed to load {title.lower()} image: {current_image}")
        if current_caption:
            st.caption(current_caption)
        st.caption(f"{current_index + 1} / {len(images)}")

    with next_col:
        st.write("")
        st.write("")
        if st.button("→", key=f"{key_prefix}_next_{app_id}", disabled=len(images) <= 1, help=f"Next {title} image"):
            st.session_state[index_key] = (current_index + 1) % len(images)
            st.rerun()


def render_app_card(app: dict, show_favorite: bool = True, show_download_toggle: bool = True, show_download_remove: bool = False):
    """
    앱 1개를 카드 형태로 렌더링합니다.
    show_favorite: 즐겨찾기 버튼 표시 여부
    """
    features = [f.strip() for f in app["features"].split("|")]
    app_id = int(app["id"])
    fav = is_favorite(app_id)
    app_store_url = str(app.get("app_store_url", "") or "").strip()
    play_store_url = str(app.get("play_store_url", "") or "").strip()

    with st.container(border=True):
        # 헤더: 이미지 or 아이콘 + 이름 + 다운로드 링크 + 다운로드 표시 버튼 + 즐겨찾기 버튼
        col_icon, col_title, col_download_link, col_download_mark, col_fav = st.columns([1, 3.8, 3.2, 2.2, 0.8])
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
        with col_download_link:
            store_links = []
            if play_store_url:
                store_links.append(("For Android", play_store_url))
            if app_store_url:
                store_links.append(("For iOS", app_store_url))

            if store_links:
                links_html = "".join(
                    f"<a href=\"{escape(url, quote=True)}\" target=\"_blank\" "
                    f"style=\"{DOWNLOAD_LINK_STYLE}\">{escape(label)}</a>"
                    for label, url in store_links
                )
                st.markdown(
                    f"<div style='display:flex;flex-direction:column;gap:6px;align-items:stretch;max-width:150px'>{links_html}</div>",
                    unsafe_allow_html=True,
                )
            else:
                st.markdown("<div style='color:#888; font-size:0.9rem'>No link</div>", unsafe_allow_html=True)

        # 다운로드 표시(사용자가 이미 다운받았는지 토글하는 버튼)
        dl = is_downloaded(app_id)
        if show_download_toggle:
            with col_download_mark:
                mark = "📥 Downloaded" if dl else "⬇️ Add to Downloaded Apps"
                if st.button(mark, key=f"dl_{app_id}", help=mark):
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
        in_app_images = _split_image_list(app.get("in_app_images", ""))
        in_app_captions = _split_caption_list(app.get("in_app_image_captions", ""))
        guide_images = _split_image_list(app.get("guide_images", ""))
        guide_captions = _split_caption_list(app.get("guide_image_captions", ""))

        gallery_buttons = []
        if in_app_images:
            gallery_buttons.append(("In App Images", in_app_images, in_app_captions, "in_app"))
        if guide_images:
            gallery_buttons.append(("How To Use", guide_images, guide_captions, "guide"))

        if gallery_buttons:
            st.markdown(GUIDE_BUTTON_STYLE, unsafe_allow_html=True)
            button_cols = st.columns([1] * len(gallery_buttons) + [6], gap="small")[:len(gallery_buttons)]
            for col, (title, images, captions, key_prefix) in zip(button_cols, gallery_buttons):
                with col:
                    _render_image_gallery_button(app_id, title, key_prefix)
            for title, images, captions, key_prefix in gallery_buttons:
                if st.session_state.get(f"gallery_active_{app_id}") == key_prefix:
                    _render_image_gallery_content(app_id, title, images, captions, key_prefix)
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
