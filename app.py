"""
app.py  ─  🏠 Main Page
실행: streamlit run app.py
"""

import streamlit as st
from components.data_loader import (
    load_apps, filter_by_category, load_favorites, get_apps_by_ids, get_top_rated_app,
    get_before_land_tips,
)
from components.app_card import render_app_card
from components.situation_helper import render_situation_helper

st.set_page_config(
    page_title="Korea Travel Apps",
    page_icon="🇰🇷",
    layout="wide",
)

# ── 헤더 ─────────────────────────────────────────────────────
col_flag, col_title = st.columns([1, 6])
with col_flag:
    st.markdown("<div style='font-size:5rem; text-align:center'>🇰🇷</div>", unsafe_allow_html=True)
with col_title:
    st.title("Korea Travel App Guide")
    st.markdown("**Your digital companion for South Korea** — curated apps that locals actually use.")

st.divider()

# ── 빠른 팁 (접이식) ──────────────────────────────────────────
with st.expander("⚡ Before You Land in Korea", expanded=False):
    default_tips = [
        "📶 Get a SIM or pocket Wi-Fi at Incheon Airport — essential for all apps below.",
        "💳 Load a **T-money card** for seamless subway & bus travel across the country.",
        "📥 Download **Papago** and **Naver Maps** offline before leaving your hotel.",
        "🚕 Install **Kakao T** before your first night — finding taxis gets much easier.",
    ]

    tips = get_before_land_tips()
    if not tips:
        tips = default_tips

    for tip in tips:
        st.markdown(tip)

st.divider()

# ── 소개 카드 그리드 ──────────────────────────────────────────
st.subheader("📌 Navigate by Topic")

pages = [
    ("📱", "Essential Apps",   "All must-have apps in one place"),
    ("🗺️", "Navigation",       "Maps, routes and local directions"),
    ("🚇", "Transportation",   "Subway, taxi, KTX & more"),
    ("🍜", "Food",             "Delivery, restaurants & dining"),
    ("🗣", "Translation",      "Break the language barrier"),
    ("🧳", "Etc.",             "Other useful travel utilities"),
    ("⭐", "Favorites",        "Your saved apps"),
    ("🎯", "Situation Helper", "Tell us your situation → get the right app"),
]


# 페이지 상태 초기화
if "page" not in st.session_state:
    st.session_state.page = "home"

cols = st.columns(4)
for i, (icon, name, desc) in enumerate(pages):
    with cols[i % 4]:
        with st.container(border=True):
            st.markdown(f"### {icon} {name}")
            st.caption(desc)
            if st.button("Open", key=f"open_{i}"):
                st.session_state.page = name
                st.rerun()

# Downloaded Apps 버튼을 내비게이션 카드 아래에 별도로 추가
with st.container():
    st.markdown("### ⬇️ Downloaded Apps")
    if st.button("Open", key="open_downloaded_special"):
        st.session_state.page = "Downloaded Apps"
        st.rerun()

st.divider()
st.caption("Data stored in `data/apps.csv` · Built with Streamlit 🎈")

# 관리 패널 임베드 렌더링
if st.session_state.page == "admin":
    from components.admin_ui import render_admin_panel
    render_admin_panel()

# 상세 페이지 렌더링
if st.session_state.page != "home" and st.session_state.page != "admin":
    sel = st.session_state.page
    # 상단 네비게이션
    col1, col2 = st.columns([9, 1])
    with col1:
        st.header(f"{sel}")
    with col2:
        if st.button("← Back"):
            st.session_state.page = "home"
            st.rerun()

    # 상황 도우미 특별 처리
    if sel == "Situation Helper":
        render_situation_helper()
    else:
        df = load_apps()
        
        # 최고 별점 앱 표시 (Favorites, Downloaded Apps, Situation Helper 제외)
        if sel not in ("Favorites", "Downloaded Apps", "Situation Helper"):
            top_app = get_top_rated_app(df, sel)
            if top_app:
                st.subheader("🌟 Top Rated App")
                render_app_card(top_app, show_favorite=True)
                st.divider()
        
        if sel == "Favorites":
            fav_ids = load_favorites()
            view_df = get_apps_by_ids(df, fav_ids)
        elif sel == "Downloaded Apps":
            from components.data_loader import load_downloads
            dl_ids = load_downloads()
            view_df = get_apps_by_ids(df, dl_ids)
        else:
            view_df = filter_by_category(df, sel)

        if view_df.empty:
            st.info("No apps found for this category.")
        else:
            st.subheader("All Apps in This Category")
            for _, row in view_df.iterrows():
                if sel == "Downloaded Apps":
                    render_app_card(row.to_dict(), show_favorite=True, show_download_toggle=True, show_download_remove=True)
                else:
                    render_app_card(row.to_dict())

# ── 관리자 접근 (페이지 하단) ──────────────────────────────────
st.divider()
with st.expander("Administrator Controls", expanded=False):
    st.markdown("Only authorized users should use these controls.")
    col_a, col_b = st.columns([1, 3])
    with col_a:
        if st.button("Open Admin Panel"):
            st.session_state.page = "admin"
            st.rerun()
    with col_b:
        st.markdown("Tip: you can also run the admin page separately with `streamlit run 9_🔧_Admin.py`.")
