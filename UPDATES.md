# 업데이트 로그 (UPDATES.md)

이 파일은 프로젝트의 변경사항(추가, 수정, 삭제)을 간단히 기록하는 로그입니다.

사용법:
- 새 변경을 적용할 때마다 날짜, 작성자(선택), 요약을 한 줄로 추가합니다.
- 필요하면 자세한 설명 또는 관련 파일 경로를 다음 줄에 작성하세요.
로그를 업데이트할 때는 위 템플릿을 사용해 변경 내역을 명확히 기록해주세요.
# UPDATES
---

## 템플릿
- 날짜: YYYY-MM-DD
- 변경자: 이름 또는 아이디
- 요약: 간단한 한 줄 요약
- 커밋 제목: 간단한 Git 커밋 메시지
- 변경 내용:
  - 항목별 상세 설명
- 관련 파일:
  - `path/to/file.py`
- 비고:
  - 추가 참고사항

---

## 0.2.01/0.2.02
- 날짜: 2026-05-22 
- 제목: Situation Helper 기능 추가 및 관리자 패널 위치 조정
- 변경자: assistant (lemonlime-orange)
- 요약: 상황 도우미(카테고리 및 상황 CRUD) 추가, 상황 접이식(expander) 적용, 관리자 컨트롤 위치 수정
- 커밋 제목: Add Situation Helper, admin UI and foldable situations
- 변경 내용:
  - `data/situations.csv`에 `category` 컬럼 추가 및 초기 상황 데이터 카테고리 지정
  - `components/data_loader.py`에 상황 관련 함수 추가: `load_situations`, `save_situations`, `get_situation_categories`, `load_situations_by_category`, `add_situation`, `update_situation`, `delete_situation`
  - 새 컴포넌트 `components/situation_helper.py` 생성: 카테고리 버튼, 카테고리별 상황 표시, 관련 앱 추천
  - `components/admin_ui.py`에 "Situation Helper" 관리 탭 추가: 목록, 추가, 편집/삭제 기능
  - `app.py`에 상황 도우미 통합: "Situation Helper" 페이지 렌더링
  - 상황 항목을 Streamlit `st.expander`로 접이식화(기본 닫힌 상태)
  - 관리자 접근 (`Administrator Controls`)을 항상 페이지 하단에 렌더되도록 이동
- 관련 파일:
  - `data/situations.csv`
  - `components/data_loader.py`
  - `components/situation_helper.py`
  - `components/admin_ui.py`
  - `app.py`


---

## 0.2.03
- 날짜: 2026-05-22
- 변경자: lemonlime-orange
- 요약: 앱 Download 버튼 생성, Before You Land in Korea 메뉴 수정 메뉴 추가
- 커밋 제목: UI 수정
- 변경 내용:
  - 🔗 Official Site로 되어있는 앱 링크를 Download Link로 즐겨찾기하는 버튼 바로 왼쪽에 파란색 버튼으로 대체
  - Administrator Controls에서 사이트 상단 Before You Land in Korea 내용을 수정할 수 있게 수정
- 관련 파일:
  - admin_ui.cpython-314.pyc
  - app_card.cpython-314.pyc
  - data_loader.cpython-314.pyc
  - admin_ui.py
  - app_card.py
  - data_loader.py
  - app.py

