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

---

## 1.0.02
- 날짜: 2026-06-06
- 변경자: lemonlime-orange
- 요약: Python 문법 검사 및 오류 수정
- 커밋 제목: python errors fixed
- 변경 내용:
  - 전체 파이썬 파일 문법 검사(py_compile) 실행
  - 9_🔧_Admin.py에서 최상단의 불필요한 공백 라인과 import 앞의 들여쓰기 제거

- 관련 파일:
  - `9_🔧_Admin.py`
- 비고: N/A

---

## 1.1.01
- 날짜: 2026-06-08
- 변경자: codex (lemonlime-orange)
- 요약: 마지막 커밋(fe18247 / 1.0.02) 이후 워킹트리 및 스테이징된 변경사항 요약
- 커밋 제목: Uncommitted changes since fe18247
- 변경 내용:
  - 여러 파일에 수정이 발생했으며 일부 파일은 새로 추가됨(아직 커밋되지 않음).
  - 주요 변경 파일(요약):
    - `components/data_loader.py`: 대규모 수정(많은 라인 추가/변경)
    - `components/admin_ui.py`: 관리자 UI 관련 수정 및 보완
    - `components/sidebar.py`: 경미한 수정
    - `app.py`: 소규모 변경
    - `requirements.txt`: 변경(줄바꿈/포맷/의존성 수정 가능성)
  - 새로 작업 중인(언트랙) 파일 및 디렉터리:
    - `.gitignore` (언트랙)
    - `.streamlit/` (언트랙 디렉터리)
    - `scripts/migrate_admin_data_to_supabase.py` (언트랙)
    - `scripts/migrate_apps_to_supabase.py` (언트랙)
    - `supabase_apps_schema.sql` (언트랙)
  - 빌드/캐시 아티팩트가 워킹트리에 존재함(예: `__pycache__` 및 .pyc 파일) — 추후 .gitignore에 추가 권장
- 관련 파일:
  - `app.py`
  - `components/admin_ui.py`
  - `components/data_loader.py`
  - `components/sidebar.py`
  - `requirements.txt`
  - `.gitignore`
  - `.streamlit/`
  - `scripts/migrate_admin_data_to_supabase.py`
  - `scripts/migrate_apps_to_supabase.py`
  - `supabase_apps_schema.sql`
  - `__pycache__/` 폴더 및 `.pyc` 파일들
- 비고:
  - 현재 변경사항은 아직 커밋되지 않았습니다. 원하시면 제가 커밋 메시지 초안을 작성하고 커밋 및 푸시까지 대신 진행해드릴 수 있습니다.

---

## 1.1.02
- 날짜: 2026-06-16
- 변경자: codex (lemonlime-orange)
- 제목: How To Use 가이드 이미지 추가 및 앱 상세 표시 기능
- 요약: 앱 상세 페이지에 "How To Use" 가이드 이미지를 첨부하고 표시하는 기능을 추가하였습니다.
- 변경 내용:
  - 앱 상세 페이지에서 가이드 이미지를 업로드하거나 표시할 수 있도록 UI 및 렌더링 로직을 추가
  - `components/app_card.py` 및 `components/data_loader.py`에 이미지 경로 로드/표시 처리 로직을 도입
  - 가이드 이미지를 `assets/images/`에 저장하도록 파일 규칙을 정리
  - 앱 메타데이터에 가이드 이미지 필드(`how_to_use_image` 등)를 반영하도록 로더/스키마를 업데이트
- 관련 파일:
  - `components/app_card.py`
  - `components/data_loader.py`
  - `app.py`
  - `assets/images/`
- 비고:
  - 권장 이미지 크기: 가로 800px 내외, 형식 PNG/JPEG 권장
  - 이미지가 없는 경우 대체 텍스트 또는 기본 안내를 표시하도록 처리됨

---

## 1.1.03
- 날짜: 2026-06-16
- 변경자: codex (lemonlime-orange)
- 제목: Admin UI 개선, 앱 카드/데이터로더 보완 및 Supabase 스키마 업데이트
- 요약: 관리자 UI 및 앱 카드 동작을 개선하고 `components/data_loader.py`의 메타데이터/이미지 로드 로직을 보완했으며, Supabase 마이그레이션용 스키마 파일을 추가/수정했습니다.
- 변경 내용:
  - `components/admin_ui.py`에서 관리자 설정 및 편집 흐름 개선(레이아웃/버튼 동작, 접근성 보완)
  - `components/app_card.py`에서 앱 카드 렌더링 개선: 가이드 이미지 처리, 다운로드/링크 동작 안정화
  - `components/data_loader.py`에서 앱 메타데이터 및 이미지 경로 로드/저장 로직을 안정화하고 예외 처리를 강화
  - `supabase_apps_schema.sql` 파일 추가 및 스키마 보완으로 Supabase로의 데이터 마이그레이션 준비
  - `UPDATES.md` 파일 업데이트(해당 변경사항 요약 추가)
- 관련 파일:
  - `components/admin_ui.py`
  - `components/app_card.py`
  - `components/data_loader.py`
  - `supabase_apps_schema.sql`
  - `UPDATES.md`
- 비고:
  - 이 변경은 최근 커밋(작성자: Lee Jumyung)에 포함된 수정 사항을 요약한 것입니다.

---

## 1.1.04
- 날짜: 2026-06-17
- 변경자: codex (lemonlime-orange)
- 제목: In App Images 기능 추가 및 관련 파일 수정
- 요약: 앱 내 이미지 업로드/저장/표시 기능(`In App Images`)을 추가하고, 이를 지원하기 위해 앱 카드, 데이터 로더, 관리자 UI 및 마이그레이션/스키마/문서를 수정함
- 커밋 제목: feat(images): add in-app images (upload, storage, display) and update loaders/admin
- 변경 내용:
  - `components/data_loader.py`:
    - 앱 메타데이터에 이미지 필드(`images`, `how_to_use_image`) 로드/저장 로직 추가
    - 이미지 파일 검증 및 로컬 저장(`assets/images/`) 유틸 함수 추가: `save_image`, `get_app_images`, `remove_app_image`
    - 기존 이미지 관련 예외 처리를 보강하고 기본값(placeholder) 처리 추가
  - `components/app_card.py`:
    - 앱 카드에서 대표 이미지 또는 썸네일을 렌더링하도록 변경
    - 앱 상세 보기에서 이미지 갤러리 또는 'How To Use' 가이드 이미지를 표시하도록 UI 보강
    - 이미지가 없을 경우 기본 플레이스홀더 이미지를 사용
  - `components/admin_ui.py`:
    - 관리자 앱 편집/등록 폼에 이미지 업로드/삭제 컨트롤 추가
    - 업로드 시 파일명 충돌 처리 및 기존 이미지와의 매핑 관리
  - `app.py`:
    - 앱 상세 페이지 및 리스트 렌더링 로직에 이미지 표시를 통합
    - 관리자 접근 시 이미지 업로드/관리 플로우를 노출
  - `assets/images/`:
    - 앱 내 이미지 저장 디렉터리 사용 규칙 명시 및 샘플/placeholder 이미지 추가(빈 디렉터리 생성/권장 사항 포함)
  - `supabase_apps_schema.sql`:
    - Supabase 마이그레이션을 위한 이미지 관련 컬럼(`images`, `how_to_use_image`) 스키마 보강
  - `scripts/migrate_apps_to_supabase.py` / `scripts/migrate_admin_data_to_supabase.py`:
    - 이미지 필드 매핑 및 파일 참조 처리 로직 추가(파일 업로드가 필요한 경우 주석으로 안내)
  - `requirements.txt`:
    - 이미지 처리/검증을 위해 `Pillow`(또는 프로젝트에서 이미 사용 중이면 주석으로 명시) 권장 의존성 추가(선택)
  - `README.md`:
    - In App Images 사용법(권장 크기, 저장 규칙, 업로드 흐름) 문서화
  - `UPDATES.md`:
    - 본 항목 추가(해당 변경사항 요약)
- 관련 파일(요약):
  - `components/data_loader.py`
  - `components/app_card.py`
  - `components/admin_ui.py`
  - `app.py`
  - `assets/images/`
  - `supabase_apps_schema.sql`
  - `scripts/migrate_apps_to_supabase.py`
  - `scripts/migrate_admin_data_to_supabase.py`
  - `README.md`
  - `requirements.txt`
  - `UPDATES.md`
- 비고:
  - 마이그레이션 스크립트는 기존 메타데이터에 이미지 경로가 포함되어 있지 않은 경우 안전하게 스킵하도록 설계됨