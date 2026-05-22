"""
admin_ui.py
관리자 패널 렌더러(재사용 가능) — `render_admin_panel()` 호출로 UI를 표시합니다.

이 모듈은 `st.set_page_config`을 호출하지 않으므로 `9_🔧_Admin.py`(단독 실행)과
`app.py`(임베드 실행)에서 모두 안전하게 임포트하여 사용할 수 있습니다.
"""

import streamlit as st
from components.data_loader import (
    load_apps, get_categories,
    add_app, update_app, delete_app,
    check_password,
    load_situations, get_situation_categories,
    add_situation, update_situation, delete_situation,
)


def render_admin_panel():
    """관리자 UI 전체를 렌더링합니다. 호출 시 Streamlit 컨텍스트 내에서 실행되어야 합니다."""
    CATEGORIES = [
        "Essential Apps",
        "Navigation",
        "Transportation",
        "Food",
        "Translation",
        "Etc.",
        "Favorites",
        "Situation Helper",
    ]
    PLATFORMS = ["iOS, Android", "iOS", "Android", "Web"]

    # 로그인 상태 관리
    if "admin_logged_in" not in st.session_state:
        st.session_state.admin_logged_in = False

    if not st.session_state.admin_logged_in:
        st.title("🔧 Admin Login")
        st.markdown("This page is for administrators only.")
        st.divider()

        col, _ = st.columns([1, 2])
        with col:
            pw = st.text_input("Password", type="password", placeholder="Enter admin password")
            if st.button("Login", use_container_width=True, type="primary"):
                if check_password(pw):
                    st.session_state.admin_logged_in = True
                    st.experimental_rerun()
                else:
                    st.error("❌ Incorrect password.")
        st.caption("Default password: `admin1234` — change `ADMIN_PASSWORD` in `components/data_loader.py`")
        st.stop()

    # 관리자 대시보드
    col_title, col_logout = st.columns([6, 1])
    with col_title:
        st.title("🔧 Admin Panel")
    with col_logout:
        st.write("")
        if st.button("Logout", type="secondary"):
            st.session_state.admin_logged_in = False
            st.experimental_rerun()

    st.divider()

    df = load_apps()

    tab_list, tab_add, tab_edit, tab_situation = st.tabs(["📋 App List", "➕ Add App", "✏️ Edit / Delete", "🎯 Situation Helper"])

    # 탭 1: 앱 목록
    with tab_list:
        st.subheader(f"📋 All Apps ({len(df)} total)")

        cats = ["All"] + sorted({
            cat.strip()
            for value in df["category"].dropna().astype(str).tolist()
            for cat in value.split("|")
            if cat.strip()
        })
        selected_cat = st.selectbox("Filter by category", cats, key="list_cat")
        if selected_cat == "All":
            view_df = df
        else:
            view_df = df[df["category"].astype(str).str.split("|").apply(
                lambda cats: selected_cat in [c.strip() for c in cats]
            )]

        display = view_df[["id", "image_url", "name", "category", "platform", "rating"]].copy()
        display.columns = ["ID", "Image URL", "Name", "Category", "Platform", "Rating"]
        st.dataframe(display, use_container_width=True, hide_index=True)

        st.caption("To edit or delete, go to the **Edit / Delete** tab.")

    # 탭 2: 추가
    with tab_add:
        st.subheader("➕ Add a New App")

        with st.form("form_add", clear_on_submit=True):
            col1, col2 = st.columns(2)

            with col1:
                name = st.text_input("App Name *", placeholder="e.g. Kakao T")
                category = st.multiselect("Categories *", CATEGORIES, default=[])
                image_url = st.text_input("Image URL *", placeholder="https://example.com/logo.png")
                platform = st.selectbox("Platform *", PLATFORMS)
                rating = st.slider("Rating", 1.0, 5.0, 4.0, 0.1)

            with col2:
                description = st.text_area("Description *", placeholder="Short description of the app...", height=100)
                download_url = st.text_input("Official Site URL *", placeholder="https://...")
                features_raw = st.text_area(
                    "Key Features * (one per line)",
                    placeholder="Taxi booking\nReal-time tracking\nFare estimate",
                    height=120,
                )
                tips = st.text_area("Travel Tip *", placeholder="A helpful tip for tourists...", height=80)

            submitted = st.form_submit_button("✅ Add App", type="primary", use_container_width=True)

        if submitted:
            missing = []
            if not name.strip():
                missing.append("Name")
            if not category:
                missing.append("Categories")
            if not image_url.strip():
                missing.append("Image URL")
            if not description.strip():
                missing.append("Description")
            if not download_url.strip():
                missing.append("URL")
            if not features_raw.strip():
                missing.append("Features")
            if not tips.strip():
                missing.append("Tips")

            if missing:
                st.error(f"❌ Please fill in: {', '.join(missing)}")
            else:
                features = "|".join(line.strip() for line in features_raw.splitlines() if line.strip())
                new_app = {
                    "name": name.strip(),
                    "category": "|".join(category),
                    "icon": "",
                    "image_url": image_url.strip(),
                    "platform": platform,
                    "rating": rating,
                    "description": description.strip(),
                    "download_url": download_url.strip(),
                    "features": features,
                    "tips": tips.strip(),
                }
                add_app(new_app)
                st.success(f"🎉 **{name}** has been added successfully!")
                st.experimental_rerun()

    # 탭 3: 편집 / 삭제
    with tab_edit:
        st.subheader("✏️ Edit or Delete an App")

        df = load_apps()

        app_options = {f"[{row['id']}] {row['name']}": row["id"] for _, row in df.iterrows()}
        selected_label = st.selectbox("Select an app to edit", list(app_options.keys()), key="edit_select")
        selected_id = app_options[selected_label]
        app = df[df["id"] == selected_id].iloc[0].to_dict()

        st.write("")

        with st.form("form_edit"):
            st.markdown(f"**Editing: {app['name']}**")
            st.write("")

            col1, col2 = st.columns(2)

            with col1:
                new_name = st.text_input("App Name", value=app["name"])
                current_cats = [c.strip() for c in str(app.get("category", "")).split("|") if c.strip()]
                new_category = st.multiselect("Categories", CATEGORIES, default=current_cats)
                new_image_url = st.text_input("Image URL", value=app.get("image_url", ""))
                new_platform = st.selectbox(
                    "Platform",
                    PLATFORMS,
                    index=PLATFORMS.index(app["platform"]) if app["platform"] in PLATFORMS else 0,
                )
                new_rating = st.slider("Rating", 1.0, 5.0, float(app["rating"]), 0.1)

            with col2:
                new_description = st.text_area("Description", value=app["description"], height=100)
                new_url = st.text_input("Official URL", value=app["download_url"])
                features_display = "\n".join(app["features"].split("|"))
                new_features_raw = st.text_area("Features (one per line)", value=features_display, height=120)
                new_tips = st.text_area("Travel Tip", value=app["tips"], height=80)

            save_btn = st.form_submit_button("💾 Save Changes", type="primary", use_container_width=True)

        if save_btn:
            missing = []
            if not new_name.strip():
                missing.append("Name")
            if not new_category:
                missing.append("Categories")
            if not new_image_url.strip():
                missing.append("Image URL")
            if not new_description.strip():
                missing.append("Description")
            if not new_url.strip():
                missing.append("URL")
            if not new_features_raw.strip():
                missing.append("Features")
            if not new_tips.strip():
                missing.append("Tips")

            if missing:
                st.error(f"❌ Please fill in: {', '.join(missing)}")
            else:
                new_features = "|".join(line.strip() for line in new_features_raw.splitlines() if line.strip())
                updated = {
                    "name": new_name.strip(),
                    "category": "|".join(new_category),
                    "icon": app.get("icon", ""),
                    "image_url": new_image_url.strip(),
                    "platform": new_platform,
                    "rating": new_rating,
                    "description": new_description.strip(),
                    "download_url": new_url.strip(),
                    "features": new_features,
                    "tips": new_tips.strip(),
                }
                update_app(selected_id, updated)
                st.success(f"✅ **{new_name}** updated successfully!")
                st.experimental_rerun()

        st.divider()
        st.markdown("#### 🗑️ Delete This App")
        st.warning(f"You are about to delete **{app['name']}**. This cannot be undone.")

        col_del, col_cancel = st.columns([1, 3])
        with col_del:
            if st.button("🗑️ Delete", type="primary", use_container_width=True, key="del_btn"):
                st.session_state["confirm_delete"] = selected_id

        if st.session_state.get("confirm_delete") == selected_id:
            st.error(f"⚠️ Are you sure you want to delete **{app['name']}**?")
            col_yes, col_no = st.columns(2)
            with col_yes:
                if st.button("Yes, delete it", type="primary", use_container_width=True):
                    delete_app(selected_id)
                    st.session_state.pop("confirm_delete", None)
                    st.success(f"🗑️ **{app['name']}** deleted.")
                    st.experimental_rerun()
            with col_no:
                if st.button("Cancel", use_container_width=True):
                    st.session_state.pop("confirm_delete", None)
                    st.experimental_rerun()

    # 탭 4: 상황 도우미 관리
    with tab_situation:
        st.subheader("🎯 Situation Helper Management")
        
        situation_categories = get_situation_categories()
        SITUATION_CATEGORIES = [
            "Navigation/Tourism Problems",
            "Translation Problems",
            "Delivery Problems",
            "Money Problems",
            "Hotel Problems",
            "Travel Problems",
            "Other Problems",
        ]
        
        sub_tab_list, sub_tab_add, sub_tab_edit = st.tabs(["📋 List", "➕ Add", "✏️ Edit / Delete"])
        
        # 서브탭 1: 상황 목록
        with sub_tab_list:
            st.subheader("📋 All Situations")
            
            cat_filter = st.selectbox("Filter by category", ["All"] + SITUATION_CATEGORIES, key="situation_cat_filter")
            
            df_situations = load_situations()
            if cat_filter != "All":
                view_situations = df_situations[df_situations["category"] == cat_filter]
            else:
                view_situations = df_situations
            
            if view_situations.empty:
                st.info("No situations found.")
            else:
                display = view_situations[["id", "situation", "emoji", "category"]].copy()
                display.columns = ["ID", "Situation", "Emoji", "Category"]
                st.dataframe(display, use_container_width=True, hide_index=True)
        
        # 서브탭 2: 상황 추가
        with sub_tab_add:
            st.subheader("➕ Add a New Situation")
            
            with st.form("form_add_situation", clear_on_submit=True):
                col1, col2 = st.columns(2)
                
                with col1:
                    sit_situation = st.text_input("Situation *", placeholder="e.g. I'm lost")
                    sit_emoji = st.text_input("Emoji *", placeholder="🗺️", max_chars=1)
                    sit_category = st.selectbox("Category *", SITUATION_CATEGORIES)
                
                with col2:
                    sit_description = st.text_area("Description *", placeholder="Describe this situation...", height=100)
                    sit_app_ids = st.text_input("App IDs (comma-separated)", placeholder="1,2,3", value="")
                
                submit_sit = st.form_submit_button("✅ Add Situation", type="primary", use_container_width=True)
            
            if submit_sit:
                missing = []
                if not sit_situation.strip():
                    missing.append("Situation")
                if not sit_emoji.strip():
                    missing.append("Emoji")
                if not sit_description.strip():
                    missing.append("Description")
                
                if missing:
                    st.error(f"❌ Please fill in: {', '.join(missing)}")
                else:
                    new_situation = {
                        "situation": sit_situation.strip(),
                        "emoji": sit_emoji.strip(),
                        "description": sit_description.strip(),
                        "category": sit_category,
                        "app_ids": sit_app_ids.strip() if sit_app_ids.strip() else "",
                    }
                    add_situation(new_situation)
                    st.success(f"🎉 **{sit_situation}** has been added successfully!")
                    st.experimental_rerun()
        
        # 서브탭 3: 상황 편집 / 삭제
        with sub_tab_edit:
            st.subheader("✏️ Edit or Delete a Situation")
            
            df_situations = load_situations()
            
            if df_situations.empty:
                st.info("No situations available to edit.")
            else:
                situation_options = {f"[{row['id']}] {row['situation']} ({row['category']})": row["id"] for _, row in df_situations.iterrows()}
                selected_sit_label = st.selectbox("Select a situation to edit", list(situation_options.keys()), key="situation_edit_select")
                selected_sit_id = situation_options[selected_sit_label]
                situation = df_situations[df_situations["id"] == selected_sit_id].iloc[0].to_dict()
                
                st.write("")
                
                with st.form("form_edit_situation"):
                    st.markdown(f"**Editing: {situation['situation']}**")
                    st.write("")
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        new_sit_situation = st.text_input("Situation", value=situation["situation"])
                        new_sit_emoji = st.text_input("Emoji", value=situation["emoji"], max_chars=1)
                        new_sit_category = st.selectbox("Category", SITUATION_CATEGORIES, index=SITUATION_CATEGORIES.index(situation["category"]))
                    
                    with col2:
                        new_sit_description = st.text_area("Description", value=situation["description"], height=100)
                        new_sit_app_ids = st.text_input("App IDs (comma-separated)", value=situation.get("app_ids", ""))
                    
                    save_sit_btn = st.form_submit_button("💾 Save Changes", type="primary", use_container_width=True)
                
                if save_sit_btn:
                    missing = []
                    if not new_sit_situation.strip():
                        missing.append("Situation")
                    if not new_sit_emoji.strip():
                        missing.append("Emoji")
                    if not new_sit_description.strip():
                        missing.append("Description")
                    
                    if missing:
                        st.error(f"❌ Please fill in: {', '.join(missing)}")
                    else:
                        updated_situation = {
                            "situation": new_sit_situation.strip(),
                            "emoji": new_sit_emoji.strip(),
                            "description": new_sit_description.strip(),
                            "category": new_sit_category,
                            "app_ids": new_sit_app_ids.strip() if new_sit_app_ids.strip() else "",
                        }
                        update_situation(selected_sit_id, updated_situation)
                        st.success(f"✅ **{new_sit_situation}** updated successfully!")
                        st.experimental_rerun()
                
                st.divider()
                st.markdown("#### 🗑️ Delete This Situation")
                st.warning(f"You are about to delete **{situation['situation']}**. This cannot be undone.")
                
                col_del, col_cancel = st.columns([1, 3])
                with col_del:
                    if st.button("🗑️ Delete", type="primary", use_container_width=True, key="del_situation_btn"):
                        st.session_state["confirm_delete_situation"] = selected_sit_id
                
                if st.session_state.get("confirm_delete_situation") == selected_sit_id:
                    st.error(f"⚠️ Are you sure you want to delete **{situation['situation']}**?")
                    col_yes, col_no = st.columns(2)
                    with col_yes:
                        if st.button("Yes, delete it", type="primary", use_container_width=True):
                            delete_situation(selected_sit_id)
                            st.session_state.pop("confirm_delete_situation", None)
                            st.success(f"🗑️ **{situation['situation']}** deleted.")
                            st.experimental_rerun()
                    with col_no:
                        if st.button("Cancel", use_container_width=True):
                            st.session_state.pop("confirm_delete_situation", None)
                            st.experimental_rerun()
