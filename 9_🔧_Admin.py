"""
9_🔧_Admin.py  ─  관리자 페이지
앱 추가 / 편집 / 삭제 기능. 비밀번호 로그인 필요.
"""

import os
import uuid
import streamlit as st
import streamlit as st
from components.admin_ui import render_admin_panel

st.set_page_config(page_title="Admin", page_icon="🔧", layout="wide")


def main():
    render_admin_panel()


if __name__ == "__main__":
    main()
                "image_url": image_path,
                "platform": new_platform,
                "rating": new_rating,
                "description": new_description.strip(),
                "download_url": new_url.strip(),
                "features": new_features,
                "tips": new_tips.strip(),
            }
            update_app(selected_id, updated)
            st.success(f"✅ **{new_name}** updated successfully!")
            st.rerun()

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
                st.rerun()
        with col_no:
            if st.button("Cancel", use_container_width=True):
                st.session_state.pop("confirm_delete", None)
                st.rerun()
