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



---

## 0.2.03
- 날짜: 2026-05-22 
- 변경자: lemonlime-orange
- 요약: 앱 Download 버튼 생성
- 커밋 제목: 앱 상세 페이지 (앱 사용 방법 이미지 첨부 기능)


---

## 0.3.01
- 날짜: 2026-06-01
- 제목: README 문서 정리 및 실행/기여/트러블슈팅 섹션 추가
- 변경자: assistant (lemonlime-orange)
- 요약: `README.md`를 재구성하여 빠른 시작, 데이터 스키마, 기여 방법, 문제 해결 항목을 추가함
- 커밋 제목: docs: reorganize README and add quickstart/contributing/troubleshooting
- 변경 내용:
  - `README.md` 전반 구조 정리 및 목차 추가
  - 설치/실행 가이드 (`pip install -r requirements.txt`, `streamlit run app.py`) 추가
  - 데이터 스키마 및 폴더 구조 명확화
  - 관리자 접근 방법, 기여 가이드, 문제 해결(Troubleshooting) 섹션 추가
- 관련 파일:
  - `README.md`
- 비고:
  - 향후 영문/일본어 번역 또는 추가 문서 요청 시 별도 업데이트 예정

---

## 0.3.02
- 날짜: 2026-06-01
- 변경자: assistant (lemonlime-orange)
- 요약: Downloaded Apps 기능 추가 및 다운로드 관리 UI 개선
- 커밋 제목: feat: add Downloaded Apps list and download-toggle UI
- 변경 내용:
  - `Downloaded Apps` 기능 추가: 사용자가 앱 상세의 새 버튼으로 다운로드 상태를 표시/토글할 수 있으며, 다운로드한 앱을 별도 목록에서 확인 가능
  - `components/data_loader.py`에 다운로드 관리 함수 추가: `load_downloads`, `save_downloads`, `is_downloaded`, `toggle_downloaded`
  - `components/app_card.py`에 다운로드 표시(토글) 버튼 추가 — 기존 Download 링크 옆에 위치, 클릭 시 `downloads.csv` 업데이트
  - `app.py`에서 `Downloaded Apps` 페이지를 별도 버튼으로 렌더링하도록 변경(내비게이션 카드 그리드 아래에 위치)
  - 다운로드 목록에서 항목 제거(Remove from Downloads) 버튼 추가
  - 초기 빈 데이터 파일 생성: `data/downloads.csv`
- 관련 파일:
  - `components/data_loader.py`
  - `components/app_card.py`
  - `app.py`
  - `data/downloads.csv`
- 비고:
  - Download 버튼 클릭과 자동 연동(클릭 시 자동으로 다운로드로 표시) 또는 다운로드 전체 삭제 기능은 향후 추가 가능

---

## 1.0.01
- 날짜: 2026-06-06
- 변경자: assistant (lemonlime-orange)
- 제목: 사용자 인증(로그인/회원가입) 및 사용자별 즐겨찾기/다운로드 저장 도입
- 요약: 기본 로그인/회원가입 기능과 사용자별 데이터 저장 구조를 추가하고 기존 favorites/downloads를 사용자별 파일로 마이그레이션하는 스크립트 및 관련 수정사항을 적용
- 커밋 제목: feat(auth): add user accounts, per-user favorites/downloads, migration
- 변경 내용:
  - 사용자 데이터 파일 추가: `data/users.csv`, `data/user_favorites.csv`, `data/user_downloads.csv`
  - 비밀번호 해싱 도입: `bcrypt` 사용 (의존성 `requirements.txt`에 추가)
  - 앱 사이드바에 로그인/회원가입 UI 추가 및 세션 기반 `st.session_state.user` 관리 (`app.py` 수정)
  - 기존 `data/favorites.csv` 및 `data/downloads.csv`를 사용자별 파일로 이전하는 마이그레이션 스크립트 추가: `scripts/migrate_to_user_files.py` (실행 시 원본 백업 생성)
  - `9_🔧_Admin.py` 파일의 손상된 내용을 정리하고 정상 실행 래퍼로 복원
  - Streamlit 실행 시 가상환경(.venv) Python을 사용하도록 권장(앱에서 `bcrypt`를 불러오기 위해 필요)
  - 마이그레이션 실행 결과: 원본 파일이 빈 상태(헤더만)이라 현재 마이그레이션된 행 없음; 스크립트는 guest 사용자(`user_id=0`)를 생성함
- 관련 파일:
  - `data/users.csv`
  - `data/user_favorites.csv`
  - `data/user_downloads.csv`
  - `scripts/migrate_to_user_files.py`
  - `app.py`
  - `requirements.txt`
  - `9_🔧_Admin.py`
- 비고:
  - 다음 권장 작업: `components.data_loader`의 `load_favorites`/`load_downloads`를 사용자별 파일로 전환, 비밀번호 정책 강화, 이메일 검증 및 비밀번호 재설정 기능 추가
