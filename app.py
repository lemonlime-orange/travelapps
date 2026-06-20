"""
app.py  ─  🏠 Main Page
실행: streamlit run app.py
"""

import streamlit as st
from components.data_loader import (
    load_apps, filter_by_category, load_favorites, get_apps_by_ids, get_top_rated_app,
    get_before_land_tips, check_password, find_user_by_username, create_user, verify_user,
)
from components.app_card import render_app_card
from components.situation_helper import render_situation_helper

st.set_page_config(
    page_title="Korea Travel Apps",
    page_icon="assets/images/travel_app_logo.png",
    layout="wide",
)


# --------------------- Authentication UI (sidebar) -----------------
if 'user' not in st.session_state:
    st.session_state.user = None

with st.sidebar:
    st.header('Account')
    if st.session_state.user:
        st.markdown(f"**Signed in:** {st.session_state.user.get('username')}")
        if st.button('Logout'):
            st.session_state.user = None
            st.experimental_rerun()
    else:
        with st.expander('Login', expanded=True):
            login_user = st.text_input('Username', key='login_user')
            login_pass = st.text_input('Password', type='password', key='login_pass')
            if st.button('Login', key='do_login'):
                ok, user = verify_user(login_user, login_pass)
                if ok:
                    st.session_state.user = user
                    st.success('Logged in')
                    st.experimental_rerun()
                else:
                    st.error('Invalid username or password')

        with st.expander('Sign up', expanded=False):
            su_user = st.text_input('Choose username', key='su_user')
            su_email = st.text_input('Email (optional)', key='su_email')
            su_pw = st.text_input('Password', type='password', key='su_pw')
            su_pw2 = st.text_input('Confirm password', type='password', key='su_pw2')
            if st.button('Create account', key='do_signup'):
                if not su_user or not su_pw:
                    st.error('Provide username and password')
                elif su_pw != su_pw2:
                    st.error('Passwords do not match')
                elif find_user_by_username(su_user):
                    st.error('Username already exists')
                else:
                    try:
                        user = create_user(su_user, su_pw, su_email)
                        st.session_state.user = user
                        st.success('Account created and signed in')
                        st.experimental_rerun()
                    except ValueError as exc:
                        st.error(str(exc))
                    except Exception as exc:
                        st.error(f'Account could not be created: {exc}')

    with st.expander("Administrator Controls", expanded=False):
        st.markdown("Authorized Users Only")
        if st.session_state.get("admin_logged_in"):
            if st.button("Open Admin Panel", key="open_admin_sidebar"):
                st.session_state.page = "admin"
                st.rerun()
            if st.session_state.get("page") == "admin":
                if st.button("Close Admin Panel", key="close_admin_sidebar"):
                    st.session_state.admin_logged_in = False
                    st.session_state.page = "home"
                    st.rerun()
        else:
            admin_password = st.text_input(
                "Password",
                type="password",
                key="admin_sidebar_password",
                placeholder="Enter admin password",
            )
            if st.button("Open Admin Panel", key="login_admin_sidebar"):
                if check_password(admin_password):
                    st.session_state.admin_logged_in = True
                    st.session_state.page = "admin"
                    st.rerun()
                else:
                    st.error("Incorrect password.")


# ── 헤더 ─────────────────────────────────────────────────────
col_flag, col_title = st.columns([1, 6])
with col_flag:
    st.image("assets/images/travel_app_logo.png", width=96)
with col_title:
    st.title("Korea Travel App Guide")
    st.markdown("**Not sure what apps you need?** — Just look here for the best apps for each situation.")

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

topic_options = [
    ("🗺️", "Navigation", "Maps, routes and local directions"),
    ("🚇", "Transportation", "Subway, taxi, KTX & more"),
    ("🍜", "Food", "Delivery, restaurants & dining"),
    ("🗣", "Translation", "Break the language barrier"),
    ("🧳", "Etc.", "Other useful travel utilities"),
]


# 페이지 상태 초기화
if "page" not in st.session_state:
    st.session_state.page = "home"

with st.container(border=True):
    st.markdown("### 📱 Essential Apps")
    st.caption("All must-have apps in one place")
    if st.button("Open Essential Apps", key="open_essential_apps", use_container_width=True):
        st.session_state.page = "Essential Apps"
        st.rerun()

with st.container(border=True):
    st.markdown("### Choose Topic")
    topic_cols = st.columns(2)
    for i, (icon, name, desc) in enumerate(topic_options):
        with topic_cols[i % 2]:
            st.caption(desc)
            if st.button(f"{icon} {name}", key=f"open_topic_{name}", use_container_width=True):
                st.session_state.page = name
                st.rerun()

with st.container(border=True):
    st.markdown("### ⬇️ Downloaded Apps")
    st.caption("Apps you've marked as downloaded")
    if st.button("Open Downloaded Apps", key="open_downloaded_special", use_container_width=True):
        st.session_state.page = "Downloaded Apps"
        st.rerun()

with st.container(border=True):
    st.markdown("### ⭐ Favorites")
    st.caption("Your saved apps")
    if st.button("Open Favorites", key="open_favorites", use_container_width=True):
        st.session_state.page = "Favorites"
        st.rerun()

st.divider()
st.subheader("🎯 Situation Helper")
with st.container(border=True):
    st.caption("Tell us your situation → get the right app")
    if st.button("Situation Categories", key="open_situation_helper", use_container_width=True):
        st.session_state.page = "Situation Helper"
        st.rerun()

st.divider()
st.caption("App data stored in Supabase · Built with Streamlit 🎈")

# 관리 패널 임베드 렌더링
if st.session_state.page == "admin":
    if st.session_state.get("admin_logged_in"):
        from components.admin_ui import render_admin_panel
        render_admin_panel()
    else:
        st.session_state.page = "home"
        st.rerun()

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
                    render_app_card(
                        row.to_dict(),
                        show_favorite=True,
                        show_download_toggle=True,
                        show_download_remove=True,
                        show_reviews=True,
                    )
                else:
                    render_app_card(row.to_dict())

