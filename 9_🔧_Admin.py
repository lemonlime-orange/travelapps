"""
9_🔧_Admin.py  ─  관리자 페이지
앱 추가 / 편집 / 삭제 기능. 비밀번호 로그인 필요.
"""

import streamlit as st
from components.admin_ui import render_admin_panel

st.set_page_config(page_title="Admin", page_icon="🔧", layout="wide")


def main():
    render_admin_panel()


if __name__ == "__main__":
    main()
