"""
app_card.py
앱 카드 UI 컴포넌트 — 즐겨찾기 토글 포함
"""

from html import escape

import streamlit as st
from components.data_loader import (
    delete_app_review,
    get_display_rating,
    get_app_review_summary,
    get_app_reviews,
    get_user_app_review,
    is_favorite,
    toggle_favorite,
    is_downloaded,
    toggle_downloaded,
    upsert_app_review,
)


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


def _legacy_render_downloaded_review_section(app_id):
    avg_rating, review_count = get_app_review_summary(app_id)
    edit_key = f"review_edit_{app_id}"

    st.divider()
    if review_count:
        st.markdown(f"**Traveler Reviews**  ⭐ {avg_rating:.1f} ({review_count})")
    else:
        st.markdown("**Traveler Reviews**")

    user = st.session_state.get("user")
    if not user:
        st.info("Log in to leave a rating and review for apps you downloaded.")
    elif not is_downloaded(app_id):
        st.info("Add this app to Downloaded Apps before leaving a review.")
    else:
        user_id = user.get("user_id", "")
        username = user.get("username", "Traveler")
        existing = get_user_app_review(app_id, user_id)
        if edit_key not in st.session_state:
            st.session_state[edit_key] = existing is None

        if existing:
            st.markdown("**My Review**")
            st.markdown(f"Rating: {float(existing.get('rating') or 0):.1f} / 5.0")
            st.markdown(
                f"<div style='color:#4b5563'>{escape(str(existing.get('review') or ''))}</div>",
                unsafe_allow_html=True,
            )
            edit_col, delete_col = st.columns([1, 1])
            with edit_col:
                edit_label = "Cancel Edit" if st.session_state[edit_key] else "Edit My Review"
                if st.button(edit_label, key=f"edit_review_{app_id}"):
                    st.session_state[edit_key] = not st.session_state[edit_key]
                    st.rerun()
            with delete_col:
                if st.button("Delete My Review", key=f"delete_review_{app_id}"):
                    delete_app_review(app_id, user_id)
                    st.session_state[edit_key] = True
                    st.success("Review deleted.")
                    st.rerun()

        if not st.session_state[edit_key]:
            st.caption("Use Edit My Review to update your rating or review.")
            return
        else:
            form_title = "Edit Review" if existing else "Write Review"
            st.markdown(f"**{form_title}**")
        default_rating = float(existing["rating"]) if existing else 4.0
        default_review = existing["review"] if existing else ""
        default_used = bool(existing["used_after_download"]) if existing else True

        with st.form(key=f"review_form_{app_id}"):
            rating = st.slider("Your rating", 0.0, 5.0, default_rating, 0.5, key=f"review_rating_{app_id}")
            used_after_download = st.checkbox(
                "I actually used this app after downloading it",
                value=default_used,
                key=f"review_used_{app_id}",
            )
            review = st.text_area(
                "Your review",
                value=default_review,
                max_chars=700,
                placeholder="What helped, what was confusing, and when would you recommend it?",
                key=f"review_text_{app_id}",
            )
            submitted = st.form_submit_button("Save Review")

        if submitted:
            if not used_after_download:
                st.warning("Please confirm that you actually used the app before leaving a review.")
            elif not review.strip():
                st.warning("Please write a short review before saving.")
            else:
                upsert_app_review(app_id, user_id, username, rating, review, used_after_download)
                st.session_state[edit_key] = False
                st.success("Review saved.")
                st.rerun()

    reviews = get_app_reviews(app_id)
    if reviews.empty:
        st.caption("No reviews yet.")
        return

    for review in reviews.to_dict("records"):
        reviewer = escape(str(review.get("username") or "Traveler"))
        text = escape(str(review.get("review") or ""))
        rating = float(review.get("rating") or 0)
        st.markdown(f"**{reviewer}** · ⭐ {rating:.1f}")
        st.markdown(f"<div style='color:#4b5563'>{text}</div>", unsafe_allow_html=True)


def _legacy_render_review_button(app_id):
    review_key = f"review_open_{app_id}"
    if review_key not in st.session_state:
        st.session_state[review_key] = False

    label = "Hide Review" if st.session_state[review_key] else "Review"
    if st.button(label, key=f"review_toggle_{app_id}", type="primary"):
        st.session_state[review_key] = not st.session_state[review_key]
        st.rerun()

    return st.session_state[review_key]


def _format_review_date(value):
    raw = str(value or "").strip()
    if not raw:
        return "Unknown date"
    return raw[:10]


def _legacy_render_review_list(app_id):
    reviews = get_app_reviews(app_id)
    if reviews.empty:
        st.caption("No user reviews yet.")
        return

    for review in reviews.to_dict("records"):
        reviewer = escape(str(review.get("username") or "Traveler"))
        text = escape(str(review.get("review") or ""))
        rating = float(review.get("rating") or 0)
        created_at = escape(_format_review_date(review.get("created_at") or review.get("updated_at")))
        st.markdown(
            (
                "<div style='border:1px solid #e5e7eb;border-radius:8px;"
                "padding:12px 14px;margin:10px 0;background:#ffffff'>"
                f"<div style='font-weight:700'>{reviewer}</div>"
                f"<div style='color:#6b7280;font-size:0.88rem'>"
                f"{created_at} · Rating {rating:.1f} / 5.0</div>"
                f"<div style='color:#374151;margin-top:8px'>{text}</div>"
                "</div>"
            ),
            unsafe_allow_html=True,
        )


def _rating_stars_html(rating):
    rating = max(0.0, min(5.0, float(rating or 0)))
    fill_width = rating / 5 * 100
    return (
        "<div style='position:relative;display:inline-block;"
        "font-size:1.45rem;line-height:1;letter-spacing:0;color:#d1d5db'>"
        "★★★★★"
        f"<div style='position:absolute;left:0;top:0;width:{fill_width:.0f}%;"
        "overflow:hidden;white-space:nowrap;color:#f59e0b'>★★★★★</div>"
        "</div>"
    )


def _render_review_list(app_id):
    reviews = get_app_reviews(app_id)
    if reviews.empty:
        st.caption("No user reviews yet.")
        return

    review_rows = reviews.to_dict("records")
    index_key = f"user_review_index_{app_id}"
    if index_key not in st.session_state:
        st.session_state[index_key] = 0

    current_index = st.session_state[index_key] % len(review_rows)
    review = review_rows[current_index]
    reviewer = escape(str(review.get("username") or "Traveler"))
    text = escape(str(review.get("review") or ""))
    rating = float(review.get("rating") or 0)
    created_at = escape(_format_review_date(review.get("created_at") or review.get("updated_at")))
    stars_html = _rating_stars_html(rating)

    prev_col, review_col, next_col = st.columns([1, 8, 1])
    with prev_col:
        st.write("")
        st.write("")
        if st.button("<", key=f"review_prev_{app_id}", disabled=len(review_rows) <= 1, help="Previous review"):
            st.session_state[index_key] = (current_index - 1) % len(review_rows)
            st.rerun()

    with review_col:
        st.markdown(
            (
                "<div style='border:1px solid #dbe3ef;border-radius:8px;"
                "padding:14px 16px;margin:8px 0;background:#ffffff;"
                "box-shadow:0 1px 2px rgba(15,23,42,0.06)'>"
                "<div style='display:flex;justify-content:space-between;gap:12px;"
                "align-items:flex-start;margin-bottom:8px'>"
                f"<div><div style='font-weight:700'>{reviewer}</div>"
                f"<div style='color:#6b7280;font-size:0.88rem'>{created_at}</div></div>"
                f"<div style='text-align:right'>{stars_html}"
                f"<div style='color:#6b7280;font-size:0.85rem;margin-top:3px'>{rating:.1f} / 5.0</div></div>"
                "</div>"
                f"<div style='color:#374151;margin-top:10px;line-height:1.55'>{text}</div>"
                f"<div style='color:#6b7280;font-size:0.82rem;margin-top:10px;text-align:center'>"
                f"{current_index + 1} / {len(review_rows)}</div>"
                "</div>"
            ),
            unsafe_allow_html=True,
        )

    with next_col:
        st.write("")
        st.write("")
        if st.button(">", key=f"review_next_{app_id}", disabled=len(review_rows) <= 1, help="Next review"):
            st.session_state[index_key] = (current_index + 1) % len(review_rows)
            st.rerun()


def _render_review_form(app_id, user_id, username, existing, edit_key):
    default_rating = float(existing["rating"]) if existing else 4.0
    default_review = existing["review"] if existing else ""
    default_used = bool(existing["used_after_download"]) if existing else True
    form_title = "Edit My Review" if existing else "Write My Review"

    st.markdown(f"**{form_title}**")
    with st.form(key=f"review_form_{app_id}"):
        rating = st.slider("Your rating", 0.0, 5.0, default_rating, 0.5, key=f"review_rating_{app_id}")
        used_after_download = st.checkbox(
            "I actually used this app after downloading it",
            value=default_used,
            key=f"review_used_{app_id}",
        )
        review = st.text_area(
            "Your review",
            value=default_review,
            max_chars=700,
            placeholder="What helped, what was confusing, and when would you recommend it?",
            key=f"review_text_{app_id}",
        )
        submitted = st.form_submit_button("Save Review")

    if submitted:
        if not used_after_download:
            st.warning("Please confirm that you actually used the app before leaving a review.")
        elif not review.strip():
            st.warning("Please write a short review before saving.")
        else:
            upsert_app_review(app_id, user_id, username, rating, review, used_after_download)
            st.session_state[edit_key] = False
            st.success("Review saved.")
            st.rerun()


def _render_downloaded_review_section(app_id):
    avg_rating, review_count = get_app_review_summary(app_id)
    edit_key = f"review_edit_{app_id}"

    st.divider()
    st.markdown("**User Reviews**")
    if review_count:
        st.caption(f"Average rating {avg_rating:.1f} / 5.0 from {review_count} user reviews")

    _render_review_list(app_id)

    user = st.session_state.get("user")
    if not user:
        st.info("Log in to leave a rating and review for apps you downloaded.")
        return
    if not is_downloaded(app_id):
        st.info("Add this app to Downloaded Apps before leaving a review.")
        return

    user_id = user.get("user_id", "")
    username = user.get("username", "Traveler")
    existing = get_user_app_review(app_id, user_id)
    if edit_key not in st.session_state:
        st.session_state[edit_key] = existing is None

    st.markdown("**Manage My Review**")
    if existing and not st.session_state[edit_key]:
        edit_col, delete_col = st.columns([1, 1])
        with edit_col:
            if st.button("Edit My Review", key=f"edit_review_{app_id}", use_container_width=True):
                st.session_state[edit_key] = True
                st.rerun()
        with delete_col:
            if st.button("Delete My Review", key=f"delete_review_{app_id}", use_container_width=True):
                delete_app_review(app_id, user_id)
                st.session_state[edit_key] = True
                st.success("Review deleted.")
                st.rerun()
        return

    if existing and st.button("Cancel Edit", key=f"cancel_review_edit_{app_id}"):
        st.session_state[edit_key] = False
        st.rerun()

    _render_review_form(app_id, user_id, username, existing, edit_key)


def _render_review_button(app_id):
    review_key = f"review_open_{app_id}"
    if review_key not in st.session_state:
        st.session_state[review_key] = False

    label = (
        "Hide Real User Reviews"
        if st.session_state[review_key]
        else "Check Real User Reviews"
    )
    if st.button(label, key=f"review_toggle_{app_id}", type="primary", use_container_width=True):
        st.session_state[review_key] = not st.session_state[review_key]
        st.rerun()

    return st.session_state[review_key]


def render_app_card(
    app: dict,
    show_favorite: bool = True,
    show_download_toggle: bool = True,
    show_download_remove: bool = False,
    show_reviews: bool = False,
):
    """
    앱 1개를 카드 형태로 렌더링합니다.
    show_favorite: 즐겨찾기 버튼 표시 여부
    """
    features = [f.strip() for f in app["features"].split("|")]
    app_id = int(app["id"])
    user = st.session_state.get("user")
    fav = is_favorite(app_id)
    display_rating, review_count, rating_source = get_display_rating(app_id, app["rating"])
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
                    f"<div style='font-size:2.2rem; text-align:center; padding-top:4px'>{app.get('app icon', app.get('icon', ''))}</div>",
                    unsafe_allow_html=True,
                )
        with col_title:
            st.markdown(f"### {app['name']}")
            rating_label = f"{display_rating:.1f}"
            if rating_source == "reviews":
                rating_label = f"{rating_label} ({review_count} reviews)"
            meta_parts = []
            developer = str(app.get("developer", "") or "").strip()
            if developer:
                meta_parts.append(f"🏢 {developer}")
            meta_parts.extend([
                f"📂 {app['category']}",
                f"📱 {app['platform']}",
                f"⭐ {rating_label}",
            ])
            st.caption("  •  ".join(meta_parts))
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
                    if not user:
                        st.session_state.auth_notice = "You Need to Sign Up to use this feature."
                        st.rerun()
                    else:
                        toggle_downloaded(app_id)
                        st.rerun()

        if show_favorite:
            with col_fav:
                star = "⭐" if fav else "☆"
                if st.button(star, key=f"fav_{app_id}", help="Add to Favorites"):
                    if not user:
                        st.session_state.auth_notice = "You Need to Sign Up to use this feature."
                        st.rerun()
                    else:
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
        st.info(f"💡 **Tips:** {app['tips']}")

        # 링크는 상단의 Download 버튼으로 대체됨

        # 다운로드 페이지에서 항목 제거 버튼
        if show_download_remove:
            if st.button("Remove from Downloads", key=f"remove_{app_id}"):
                toggle_downloaded(app_id)
                st.rerun()

        if show_reviews and _render_review_button(app_id):
            _render_downloaded_review_section(app_id)
