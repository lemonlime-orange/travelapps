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
    upload_internal_asset,
    get_display_rating,
    check_password,
    load_situations, get_situation_categories,
    add_situation, update_situation, delete_situation,
)
from components.data_loader import get_before_land_tips, update_before_land_tips


def _split_lines_preserve_order(text):
    return [line.strip() for line in str(text or "").splitlines()]


def _split_pipe_preserve_order(text):
    return [part.strip() for part in str(text or "").split("|")]


def _join_pipe_preserve_order(values):
    return "|".join(str(value or "").strip() for value in values)


def _first_store_url(app_store_url, play_store_url):
    return app_store_url.strip() or play_store_url.strip()


def _initial_store_urls(app):
    app_store_url = str(app.get("app_store_url", "") or "").strip()
    play_store_url = str(app.get("play_store_url", "") or "").strip()

    return app_store_url, play_store_url


def _match_captions_to_images(captions, image_count):
    captions = list(captions)
    if len(captions) < image_count:
        captions.extend([""] * (image_count - len(captions)))
    return captions[:image_count]


def _dataframe_height(row_count):
    return max(240, (int(row_count) + 1) * 35 + 3)


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
        st.caption("change `ADMIN_PASSWORD` in `components/data_loader.py`")
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

    df = load_apps(use_service_role=True)

    tab_list, tab_add, tab_edit, tab_situation, tab_before = st.tabs(["📋 App List", "➕ Add App", "✏️ Edit / Delete", "🎯 Situation Helper", "📝 Before You Land"])

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

        display = view_df.copy()
        if not display.empty:
            display["rating"] = display.apply(
                lambda row: get_display_rating(row["id"], row["rating"])[0],
                axis=1,
            )
        st.dataframe(
            display,
            use_container_width=True,
            hide_index=True,
            height=_dataframe_height(len(display)),
        )

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
                rating = st.slider("Rating", 0.0, 5.0, 4.0, 0.1)

            with col2:
                description = st.text_area("Description *", placeholder="Short description of the app...", height=100)
                app_store_url = st.text_input("Apple App Store URL", placeholder="https://apps.apple.com/...")
                play_store_url = st.text_input("Google Play Store URL", placeholder="https://play.google.com/store/apps/details?id=...")
                features_raw = st.text_area(
                    "Key Features * (one per line)",
                    placeholder="Taxi booking\nReal-time tracking\nFare estimate",
                    height=120,
                )
                tips = st.text_area("Travel Tip *", placeholder="A helpful tip for tourists...", height=80)
                in_app_uploads = st.file_uploader("In-App Images (upload files)", accept_multiple_files=True, type=["png", "jpg", "jpeg", "gif", "webp"])
                in_app_urls = st.text_area("In-App Image URLs (one per line)", placeholder="https://example.com/screen1.png\nhttps://...", height=80)
                in_app_captions = st.text_area(
                    "In-App Image Captions (one line per image)",
                    placeholder="Home screen\nSearch results",
                    help="Captions are matched to in-app images by line number. Leave a blank line if an image should have no caption.",
                    height=80,
                )
                guide_uploads = st.file_uploader("Guide Images (upload files)", accept_multiple_files=True, type=["png", "jpg", "jpeg", "gif", "webp"]) 
                guide_urls = st.text_area("Guide Image URLs (one per line)", placeholder="https://example.com/step1.png\nhttps://...", height=80)
                guide_captions = st.text_area(
                    "Guide Image Captions (one line per image)",
                    placeholder="Step 1: Open the app\nStep 2: Tap 'Start'",
                    help="Captions are matched to guide images by line number. Leave a blank line if an image should have no caption.",
                    height=80,
                )

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
            if not _first_store_url(app_store_url, play_store_url):
                missing.append("Apple App Store URL or Google Play Store URL")
            if not features_raw.strip():
                missing.append("Features")
            if not tips.strip():
                missing.append("Tips")

            if missing:
                st.error(f"❌ Please fill in: {', '.join(missing)}")
            else:
                features = "|".join(line.strip() for line in features_raw.splitlines() if line.strip())

                # 업로드 파일 저장
                in_app_paths = []
                img_paths = []
                upload_errors = []
                if in_app_uploads:
                    for f in in_app_uploads:
                        try:
                            in_app_paths.append(upload_internal_asset(f, "in-app-images"))
                        except Exception as exc:
                            upload_errors.append(f"{f.name}: {exc}")

                for line in (in_app_urls or "").splitlines():
                    line = line.strip()
                    if line:
                        in_app_paths.append(line)

                if guide_uploads:
                    for f in guide_uploads:
                        try:
                            img_paths.append(upload_internal_asset(f, "guide-images"))
                        except Exception as exc:
                            upload_errors.append(f"{f.name}: {exc}")

                # 텍스트로 입력된 URL 추가
                for line in (guide_urls or "").splitlines():
                    line = line.strip()
                    if line:
                        img_paths.append(line)

                in_app_images_value = "|".join(in_app_paths)
                guide_images_value = "|".join(img_paths)

                # 캡션 처리 (각 라인 하나의 캡션, 이미지 순서와 매칭)
                in_app_caption_rows = _match_captions_to_images(_split_lines_preserve_order(in_app_captions), len(in_app_paths))
                in_app_captions_value = _join_pipe_preserve_order(in_app_caption_rows)
                captions = _match_captions_to_images(_split_lines_preserve_order(guide_captions), len(img_paths))
                guide_captions_value = _join_pipe_preserve_order(captions)

                if upload_errors:
                    st.error("Images could not be uploaded to Supabase Storage.")
                    for message in upload_errors:
                        st.caption(message)
                    st.stop()
                else:
                    new_app = {
                        "name": name.strip(),
                        "category": "|".join(category),
                        "icon": "",
                        "image_url": image_url.strip(),
                        "platform": platform,
                        "rating": rating,
                        "description": description.strip(),
                        "app_store_url": app_store_url.strip(),
                        "play_store_url": play_store_url.strip(),
                        "features": features,
                        "tips": tips.strip(),
                        "in_app_images": in_app_images_value,
                        "in_app_image_captions": in_app_captions_value,
                        "guide_images": guide_images_value,
                        "guide_image_captions": guide_captions_value,
                    }
                    if not add_app(new_app):
                        st.stop()
                st.success(f"🎉 **{name}** has been added successfully!")
                st.experimental_rerun()

    # 탭 3: 편집 / 삭제
    with tab_edit:
        st.subheader("✏️ Edit or Delete an App")

        df = load_apps(use_service_role=True)

        if df.empty:
            st.info("No apps are available to edit yet. Add an app or run the Supabase migration first.")
            st.stop()

        app_options = {f"[{row['id']}] {row['name']}": row["id"] for _, row in df.iterrows()}
        selected_label = st.selectbox("Select an app to edit", list(app_options.keys()), key="edit_select")
        selected_id = app_options[selected_label]
        app = df[df["id"] == selected_id].iloc[0].to_dict()
        current_app_store_url, current_play_store_url = _initial_store_urls(app)
        display_rating, rating_review_count, rating_source = get_display_rating(selected_id, app["rating"])
        new_rating = float(app["rating"])

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
                if rating_source == "reviews":
                    st.markdown("**Rating**")
                    st.info(
                        f"Using review average: {display_rating:.1f} / 5.0 "
                        f"from {rating_review_count} registered ratings."
                    )
                else:
                    new_rating = st.slider("Rating", 0.0, 5.0, float(app["rating"]), 0.1)

            with col2:
                new_description = st.text_area("Description", value=app["description"], height=100)
                new_app_store_url = st.text_input("Apple App Store URL", value=current_app_store_url)
                new_play_store_url = st.text_input("Google Play Store URL", value=current_play_store_url)
                features_display = "\n".join(app["features"].split("|"))
                new_features_raw = st.text_area("Features (one per line)", value=features_display, height=120)
                new_tips = st.text_area("Travel Tip", value=app["tips"], height=80)
                current_in_app_imgs = [s.strip() for s in str(app.get("in_app_images", "") or "").split("|") if s.strip()]
                current_in_app_captions = _split_pipe_preserve_order(app.get("in_app_image_captions", ""))
                if current_in_app_imgs:
                    st.markdown("**Current In-App Images**")
                    cols_preview = st.columns(min(3, len(current_in_app_imgs)))
                    for i, img in enumerate(current_in_app_imgs):
                        try:
                            cols_preview[i % 3].image(img, width=200)
                        except Exception:
                            cols_preview[i % 3].markdown(f"Failed to load: {img}")
                        caption = current_in_app_captions[i] if i < len(current_in_app_captions) else ""
                        if caption:
                            cols_preview[i % 3].caption(caption)
                new_in_app_uploads = st.file_uploader("In-App Images (upload new files to add)", accept_multiple_files=True, type=["png", "jpg", "jpeg", "gif", "webp"])
                new_in_app_text = st.text_area("In-App Image URLs (one per line)", value="\n".join(current_in_app_imgs), height=80)
                new_in_app_captions = st.text_area(
                    "In-App Image Captions (one line per image)",
                    value="\n".join(current_in_app_captions[:len(current_in_app_imgs)]),
                    help="Captions are matched to in-app images by line number. Leave a blank line if an image should have no caption.",
                    height=80,
                )
                # 기존 가이드 이미지 및 캡션 불러오기
                current_imgs = [s.strip() for s in str(app.get("guide_images", "") or "").split("|") if s.strip()]
                current_captions = _split_pipe_preserve_order(app.get("guide_image_captions", ""))
                if current_imgs:
                    st.markdown("**Current Guide Images**")
                    cols_preview = st.columns(min(3, len(current_imgs)))
                    for i, img in enumerate(current_imgs):
                        try:
                            cols_preview[i % 3].image(img, width=200)
                        except Exception:
                            cols_preview[i % 3].markdown(f"Failed to load: {img}")
                        caption = current_captions[i] if i < len(current_captions) else ""
                        if caption:
                            cols_preview[i % 3].caption(caption)
                new_guide_uploads = st.file_uploader("Guide Images (upload new files to add)", accept_multiple_files=True, type=["png", "jpg", "jpeg", "gif", "webp"])                
                new_guide_text = st.text_area("Guide Image URLs (one per line)", value="\n".join(current_imgs), height=80)
                new_guide_captions = st.text_area(
                    "Guide Image Captions (one line per image)",
                    value="\n".join(current_captions[:len(current_imgs)]),
                    help="Captions are matched to guide images by line number. Leave a blank line if an image should have no caption.",
                    height=80,
                )

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
            if not _first_store_url(new_app_store_url, new_play_store_url):
                missing.append("Apple App Store URL or Google Play Store URL")
            if not new_features_raw.strip():
                missing.append("Features")
            if not new_tips.strip():
                missing.append("Tips")

            if missing:
                st.error(f"❌ Please fill in: {', '.join(missing)}")
            else:
                new_features = "|".join(line.strip() for line in new_features_raw.splitlines() if line.strip())

                # 새로 업로드된 파일 저장 및 텍스트로 입력된 URL 합치기
                updated_in_app_paths = []
                updated_img_paths = []
                upload_errors = []
                for line in (new_in_app_text or "").splitlines():
                    line = line.strip()
                    if line:
                        updated_in_app_paths.append(line)

                if new_in_app_uploads:
                    for f in new_in_app_uploads:
                        try:
                            updated_in_app_paths.append(upload_internal_asset(f, "in-app-images"))
                        except Exception as exc:
                            upload_errors.append(f"{f.name}: {exc}")

                for line in (new_guide_text or "").splitlines():
                    line = line.strip()
                    if line:
                        updated_img_paths.append(line)

                if new_guide_uploads:
                    for f in new_guide_uploads:
                        try:
                            updated_img_paths.append(upload_internal_asset(f, "guide-images"))
                        except Exception as exc:
                            upload_errors.append(f"{f.name}: {exc}")

                in_app_images_combined = "|".join(updated_in_app_paths)
                guide_images_combined = "|".join(updated_img_paths)

                # 새 캡션 처리
                updated_in_app_captions = _match_captions_to_images(
                    _split_lines_preserve_order(new_in_app_captions),
                    len(updated_in_app_paths),
                )
                in_app_captions_combined = _join_pipe_preserve_order(updated_in_app_captions)
                updated_captions = _match_captions_to_images(
                    _split_lines_preserve_order(new_guide_captions),
                    len(updated_img_paths),
                )
                guide_captions_combined = _join_pipe_preserve_order(updated_captions)

                if upload_errors:
                    st.error("Images could not be uploaded to Supabase Storage.")
                    for message in upload_errors:
                        st.caption(message)
                    st.stop()

                updated = {
                    "name": new_name.strip(),
                    "category": "|".join(new_category),
                    "icon": app.get("icon", ""),
                    "image_url": new_image_url.strip(),
                    "platform": new_platform,
                    "rating": new_rating,
                    "description": new_description.strip(),
                    "app_store_url": new_app_store_url.strip(),
                    "play_store_url": new_play_store_url.strip(),
                    "features": new_features,
                    "tips": new_tips.strip(),
                    "in_app_images": in_app_images_combined,
                    "in_app_image_captions": in_app_captions_combined,
                    "guide_images": guide_images_combined,
                    "guide_image_captions": guide_captions_combined,
                }
                if not update_app(selected_id, updated):
                    st.stop()
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

        # 탭: Before You Land 편집
        with tab_before:
            st.subheader("📝 Edit 'Before You Land in Korea' Tips")

            current = get_before_land_tips()
            default_text = "\n".join(current) if current else "📶 Get a SIM or pocket Wi-Fi at Incheon Airport — essential for all apps below.\n💳 Load a **T-money card** for seamless subway & bus travel across the country.\n📥 Download **Papago** and **Naver Maps** offline before leaving your hotel.\n🚕 Install **Kakao T** before your first night — finding taxis gets much easier."

            with st.form("form_before_land"):
                st.markdown("Tips: 입력 시 각 라인 하나의 팁으로 취급됩니다. 이모지를 포함할 수 있습니다.")
                tips_text = st.text_area("Tips (one per line)", value=default_text, height=200)
                save_tips = st.form_submit_button("💾 Save Tips", type="primary")

            if save_tips:
                new_tips = [line.strip() for line in tips_text.splitlines() if line.strip()]
                update_before_land_tips(new_tips)
                st.success("✅ 'Before You Land' tips updated.")
                st.experimental_rerun()
