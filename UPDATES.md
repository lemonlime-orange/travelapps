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

---

## 1.1.05
- 날짜: 2026-06-17
- 변경자: codex (lemonlime-orange)
- 제목: Administrator Controls 위치/접근 방법 개선
- 요약: `Administrator Controls` 메뉴의 위치를 사이드바로 이동하고 접근 제어 및 단축키/모달 형태의 빠른 접근을 추가함
- 커밋 제목: feat(admin): relocate Administrator Controls to sidebar and add access controls
- 변경 내용:
  - `components/sidebar.py`에 `Administrator Controls` 링크를 추가하여 관리자 전용 메뉴를 사이드바에 노출하도록 
  - `components/admin_ui.py`의 관리자 패널 렌더링을 페이지 하단에서 분리하여 사이드바 링크 클릭 시 전용 페이지 또는 모달로 열리게 변경
  - 접근 제어를 도입: `st.session_state.user`의 `is_admin` 플래그(또는 `components/data_loader.py`의 사용자 권한 검사)를 기반으로 메뉴 노출 및 접근을 제한
  - 관리자 빠른 액세스: 관리자 전용 단축키(`Ctrl+Alt+A` 기본값, 설정에서 변경 가능)를 추가하여 모달로 즉시 접근 가능하게 구현
  - `app.py`에서 관리자 권한 체크 및 라우팅 통합, 비관리자 접근 시 숨김 및 예외 처리 추가
  - 문서(README) 및 앱 내 도움말에 관리자 접근 방법(사이드바, 단축키, 권한 필요) 설명 추가
- 관련 파일:
  - `components/sidebar.py`
  - `components/admin_ui.py`
  - `app.py`
  - `components/data_loader.py`
  - `README.md`
- 비고:
  - 기존에 페이지 하단에 항상 렌더되던 관리자 컨트롤은 제거되었으며, 사이드바에 관리자 전용 링크가 없으면 공간을 차지하지 않음
 
---

## 1.2.01
- 날짜: 2026-06-17
- 변경자: codex (lemonlime-orange)
- 제목: 리뷰(평점/댓글) 기능 추가
- 요약: 앱 상세에서 리뷰 작성 및 조회, 평점 집계 기능을 도입
- 커밋 제목: feat(reviews): add reviews (rating/comment) feature
- 변경 내용:
  - `data/app_reviews.csv`를 사용하여 리뷰(작성자, 앱아이디, 평점, 댓글, 생성일) 저장 및 로드 기능 추가
  - `components/data_loader.py`에 리뷰 관련 함수 추가: `load_reviews`, `save_review`, `get_reviews_for_app`, `get_average_rating_for_app`
  - `components/app_card.py` 및 앱 상세 뷰에 리뷰 요약(평균 평점, 리뷰 수) 표시 및 '리뷰 보기/작성' 버튼 추가
  - `components/admin_ui.py`에 리뷰 관리 탭 추가: 리뷰 목록 조회 및 삭제 기능
  - `app.py`에 리뷰 작성 폼(평점 선택, 텍스트 입력)과 리뷰 목록 렌더링 통합
- 관련 파일:
  - `data/app_reviews.csv`
  - `components/data_loader.py`
  - `components/app_card.py`
  - `components/admin_ui.py`
  - `app.py`
- 비고:
  - 초기 `data/app_reviews.csv`가 존재하므로 빈 파일이거나 기존 데이터와 호환되도록 로더는 안전하게 파싱하도록 설계함

 
---

## 1.2.02
- 날짜: 2026-06-17
- 변경자: codex (lemonlime-orange)
- 제목: 리뷰 기능 개선 및 버그 수정
- 요약: 리뷰 저장/표시 로직 안정화, 평균 평점 집계 기준 적용, 관리자 리뷰 통계 표시 추가
- 커밋 제목: fix(reviews): stabilize review storage/display and admin stats
- 변경 내용:
  - 리뷰 저장/로딩의 안정성 개선 및 CSV 헤더 정합성 보강
  - 평균 평점 표시 로직에 최소 리뷰수 기준(`MIN_REVIEWS_FOR_AVERAGE_RATING`) 적용
  - 사용자 리뷰 CRUD(작성/수정/삭제) 흐름 검증 및 폼 유효성 강화
  - `components/admin_ui.py`에 리뷰 통계(평균 평점, 리뷰 수) 표시 추가
  - `components/app_card.py`의 리뷰 렌더링/메시지(로그인 안내, 사용 확인 문구) 소소한 UI 개선
- 관련 파일:
  - `data/app_reviews.csv`
  - `components/data_loader.py`
  - `components/app_card.py`
  - `components/admin_ui.py`
  - `app.py`
- 비고:
  - 향후: 리뷰 신고/필터, 편집 기록(audit) 및 페이징/정렬 옵션 추가 고려

---

## 1.3.01
- 날짜: 2026-06-17
- 변경자: codex (lemonlime-orange)
- 제목: 사용자 및 리뷰 데이터 Supabase 이전
- 요약: 유저 계정/즐겨찾기/다운로드와 리뷰 데이터를 Supabase로 마이그레이션하는 스크립트 및 스키마 지원을 도입
- 커밋 제목: feat(supabase): migrate user and review data to Supabase
- 변경 내용:
  - `scripts/migrate_user_data_to_supabase.py` 추가/확장: `users.csv`, `user_favorites.csv`, `user_downloads.csv`, `app_reviews.csv`를 Supabase로 업서트
  - `components/data_loader.py`에서 Supabase 클라이언트 및 설정 로딩 로직을 유지하여 앱이 Supabase 환경에서도 사용자 데이터와 리뷰 데이터를 읽을 수 있도록 준비
  - `supabase_apps_schema.sql` 및 관련 스키마 정의 수정으로 `app_reviews`, `user_favorites`, `user_downloads`, `app_users` 테이블 구조를 지원
  - 앱 리뷰 마이그레이션은 기존 로컬 `user_id`를 Supabase에 업서트된 사용자 ID로 매핑하여 참조 무결성을 유지
  - `data/app_reviews.csv`를 기반으로 리뷰 평점/댓글 데이터가 Supabase `app_reviews` 테이블에 통합되도록 변환 및 업서트 처리
- 관련 파일:
  - `scripts/migrate_user_data_to_supabase.py`
  - `components/data_loader.py`
  - `supabase_apps_schema.sql`
  - `data/app_reviews.csv`
  - `data/users.csv`
  - `data/user_favorites.csv`
  - `data/user_downloads.csv`
- 비고:
  - 로컬 CSV가 없거나 값이 비어 있는 레코드는 안전하게 건너뛰도록 설계됨

  ---

## 1.4.01
- 날짜: 2026-06-20
- 변경자: codex (lemonlime-orange)
- 제목: 제목 수정 및 로고 변경
- 요약: 부제목 수정 및 로고 수정
- 커밋 제목: Sub-Title Change with Logo Update
- 변경 내용:
  - 부제목 Not sure what apps you need? — Just look here for the best apps for each situation. 로 수정
  - 로고 Travel과 App의 컨셉을 담을 수 있도록 수정
- 관련 파일:
  - `assets\images\travel_app_logo.png`
  - `components\__pycache__\app_card.cpython-314.pyc`
  - `components\sidebar.py`
  - `app.py`
- 비고:
  - 추가 UI 수정 예정 (폰트 및 항목 배치)
  
  ---

## 1.4.02
- 날짜: 2026-06-20
- 변경자: codex (lemonlime-orange)
- 제목: 버튼 위치 수정 밑 섹션 재구성
- 요약: 섹션 재구성 밑 버튼 위치/이름 수정
- 커밋 제목: Changes to sections and small UI changes
- 변경 내용:
  - Situation Helper 별도 섹션으로 분리
  - 원래 8개 항목으로 되어있던 버튼들을 Choose Topic에 5개를 묶어서 배치
  - Essential Apps, Downloaded Apps, Favorites는 길게 배치.
- 관련 파일:
  - `app.py`
  - `__pycache__\app.cpython-314.pyc`
- 비고:
  - 추가 UI/UA 수정 예정 (폰트 등)

  ---

## 1.4.03
- 날짜: 2026-06-20
- 변경자: codex (lemonlime-orange)
- 제목: 폰트 수정
- 요약: DoHyeon, Quicksand로 폰트 수정
- 커밋 제목: Font Changes
- 변경 내용:
  - 제목/부제목 등은 DoHyeon으로 수정
  - 제목은 font-weight를 600~700으로, 부제목은 500으로 수정
  - 나머지 본문 내용 등은 Quicksand로 통일
  - Quicksand는 font-weight를 400으로 통일
  - Essential Apps, Downloaded Apps, Favorites는 길게 배치.
- 관련 파일:
  - `app.py`
  - `__pycache__\app.cpython-314.pyc`
  - `assets\fonts\DoHyeon-Regular.ttf`
  - `assets\fonts\OFL-DoHyeon.txt`
  - `assets\fonts\Quicksand-wght.ttf`
  - `assets\fonts\OFL-Quicksand.txt`
- 비고:
  - 1차 UI/UA 수정 완료 (폰트, 섹션 분리, 버튼 배치, 제목/부제목, 로고 등)
  
 ---

## 1.4.04
- 날짜: 2026-06-20
- 변경자: codex (lemonlime-orange)
- 제목: Minor fixes
- 요약: Minor fixes
- 커밋 제목: Minor fixes
- 변경 내용:
  - Catagories에서 Tips 분류를 etc. 으로 명칭을 바꿈
  - Supabase에서도 같은 수정사항 적용
- 관련 파일:
  - `admin_ui.py`
  - `apps.csv`
- 비고:

 ---
## 1.4.05
- 날짜: 2026-07-10
- 변경자: codex (lemonlime-orange)
- 제목: Minor Data Form Edits
- 요약: Added 'Developers' to app information
- 커밋 제목: Data Form Edit
- 변경 내용:
  - Developer 항목을 앱 정보에 추가
  - Supabase에서도 같은 수정사항 적용
  - 추후 계획되어 있는 앱 정보 대량 수정을 위해 Supabase Table 일부 수정
- 관련 파일:
  - `admin_ui.py`
  - `app_card.csv`
  - `data_loader.py`
  - `migrate_apps_to_supabase.py`
  - `admin_ui.cpython-314.pyc`
  - `app_card.cpython-314.pyc`
  - `data_loader.cpython-314.pyc`
  - `supabase_apps_schema.sql`
- 비고: 앱 정보 대량 수정 추후 계획되어 있음


 ---
## 1.5.01
- 날짜: 2026-07-11
- 변경자: codex (lemonlime-orange)
- 제목: Account Features Added
- 요약: Added Features When Logged In
- 커밋 제목: Log-in Faetures
- 변경 내용:
  - 테스트 계정(test_traveler) 추가
  - 로그인 후 화면에 아무것도 뜨지 않던 현상 수정
  - Downloaded Apps/Favorites 메뉴는 로그인 후에만 뜰 수 있게 수정
  - Favorites/Downloaded 메뉴에 로그인 후 해당 버튼 누르면 추가되게 확인
  - Supabase에 Favorites/Downloaded 유저별 데이터 저장 여부 점검
  - Add to Favorites/Add to Downloaded Apps에 추가할 때, 로그인 되지 않았으면, "You Need to Sign Up to use this feature."이라는 경고 메세지 뜨는 기능 추가
  - 위에 경고 메세지 뜨는 위치 등 수정
  - Tip로 뜨던 것들 Tips로 전부 수정
- 관련 파일:
  - `app.py`
  - `app_card.csv`
  - `data_loader.py`
  - `app_card.cpython-314.pyc`
  - `data_loader.cpython-314.pyc`
  - `users.csv`
- 비고: 앱 정보 대량 수정 추후 계획되어 있음

 ---

## 1.5.02
- 날짜: 2026-07-12
- 변경자: codex (lemonlime-orange)
- 제목: Changes to Essential Apps
- 요약: Essential App Information is Saved in a Different Way
- 커밋 제목: Essential App Changes
- 변경 내용:
  - Essential App는 원래 Category를 통해 설정하는 형태였음
  - essential_apps라는 새 Supabase 테이블 생성
  - app_id와 created_at 정보 포함
  - apps.csv에서 정보 가져옴
  - 체크박스로 추가할 수 있게 함
  - 공개되서는 안되는 정보가 푸시되고 있어서, 가정보로 수정
- 관련 파일:
  - `app.py`
  - `admin_ui.py`
  - `data_loader.py`
  - `secrets.example.toml`
  - `supabase_apps_schema.sql`
- 비고: 

 ---

## 1.5.03
- 날짜: 2026-07-12
- 변경자: codex (lemonlime-orange)
- 제목: README.md Update
- 요약: README.md Update to match recent updates/changes
- 커밋 제목: README.md Update
- 변경 내용:
  - README.md를 UPDATES.md 등을 토대로 수정
  - README.md를 현재 구현에 맞게 수정
- 관련 파일: 
  - `README.md`
  - `UPDATES.md`

  ---

## 1.6.01
- 날짜: 2026-07-13
- 변경자: codex (lemonlime-orange)
- 제목: Large Data Update with Essential App Feature edited
- 요약: Added new apps with confirmed data
- 커밋 제목: Large Data Update with Essential App Feature edited
- 변경 내용:
  - 앱 데이터 추가 및 기존 데이터 이동/삭제
  - 없어진 앱의 데이터는 삭제, id가 바뀐 앱의 데이터는 이동
  - Essential Apps에 선정 이유 기능 추가
  - Supabase에 essential_apps 테이블에 why_essential column 추가
  - 그 외 소규모 error들 수정
- 관련 파일:
  - `app.py`
  - `data_loader.py`
  - `admin_ui.py`
  - `app_card.py`
  - `migrate_apps_to_supabase.py`
  - `app.cpython-314.pyc`
  - `admin_ui.cpython-314.pyc`
  - `app_card.cpython-314.pyc`
  - `data_loader.cpython-314.pyc`
  - `apps.csv`
  - `README.md`
  - `supabase_apps_schema.sql`
  - `reconcile_replaced_app_ids.sql`
- 비고:
  - Supabase에서 app-data edit(4) 절대 재실행하지 말것(파일 구조 깨질 수 있음)
  - Essential App으로 지정할 경우 선정 이유 필수 작성.

 ---

## 1.6.02
- 날짜: 2026-07-13
- 변경자: codex (lemonlime-orange)
- 제목: Before You Land in Korea Changes
- 요약: ⚡ Before You Land in Korea Format Edited
- 커밋 제목: Before You Land in Korea Changes
- 변경 내용:
  - Before You Land in Korea 시스템을 원래의 드롭다운만 되는 형태에서 드롭다운 및 단계별로 나누어 옆으로 넘길 수 있는 형태로 바꿈
  - 내용 작성 및 단계 추가 Administator Controls에서 가능
- 관련 파일: 
  - `app.py`
  - `admin_ui.py`
  - `data_loader.py`
  - `app.cpython-314.pyc`
  - `admin_ui.cpython-314.pyc`
  - `data_loader.cpython-314.pyc`
  - `sidebar.cpython-314.pyc`
- 비고:
  - 작업 과정 Supabase 데이터와 일부 호환 오류가 나서, 수정 후 정상화

  ---

## 1.6.03
- 날짜: 2026-07-14
- 변경자: codex (lemonlime-orange)
- 제목: Before You Land in Korea Changes
- 요약: ⚡ Before You Land in Korea data stored in new data table
- 커밋 제목: Before You Land in Korea Changes to Data Storage
- 변경 내용:
  - Before You Land in Korea 내용의 데이터가 app_setting 1칸에 전부 들어가, 로딩이 매우 느렸음
  - before_land_steps Supabase 테이블에 데이터가 저장되게 함
  - id, title, content, position로 열 구성
  - 기존 app_settings.before_land 데이터 삭제
- 관련 파일: 
  - `data_loader.py`
  - `data_loader.cpython-314.pyc`
  - `migrate_admin_data_to_supabase.py`
  - `supabase_apps_schema.sql`
- 비고:
  - 기존 데이터는 사용자 요청에 의해 삭제

  ---

## 1.6.04
- 날짜: 2026-07-14
- 변경자: codex (lemonlime-orange)
- 제목: Before You Land in Korea Minor Changes
- 요약: ⚡ Before You Land in Korea minor changes in Data Storage
- 커밋 제목: Before You Land in Korea Minor Changes to Data Storage
- 변경 내용:
  - Before You Land in Korea 내용을 담은 before_land_steps 약간 수정
  - id 행 저장 방식 UUID -> (bigint 1,2,3, ...의 정수 ID로 변환)
  - position 넘버링이 0부터 시작하던 것을 1부터 시작하게 수정
- 관련 파일: 
  - `data_loader.py`
  - `data_loader.cpython-314.pyc`
  - `migrate_admin_data_to_supabase.py`
  - `supabase_apps_schema.sql`
- 비고:
  - UUID에서 bigint 방식으로 바꿨으므로 여러 사용자 동시 수정 주의 필요

  ---

## 1.6.05
- 날짜: 2026-07-14
- 변경자: codex (lemonlime-orange)
- 제목: Minor Fixes
- 요약: Minor Fixes
- 커밋 제목: Minor Fixes
- 변경 내용:
  - sidebar가 접힐때, 접고 여는 화살표가 아이콘 대신 글씨로 깨져 나오던 현상 수정
  - ⚡ Before You Land in Korea의 양 끝에서는 더 이상 넘길 수 없게 수정
  - 가장 하단의 App data stored in Supabase · Built with Streamlit 🎈 을 This is made available by Supabase & Streamlit 로 수정
- 관련 파일: 
  - `app.py`
  - `app.cpython-314.pyc`
  - `sidebar.py`
  - `sidebar.cpython-314.pyc`
- 비고:
  - 소규모 수정사항들 수정 및 보완

  ---

## 1.6.06
- 날짜: 2026-07-14
- 변경자: codex (lemonlime-orange)
- 제목: Situation Helper Error Fix
- 요약: Situation Helper Error Fix
- 커밋 제목: Situation Helper Error Fix
- 변경 내용:
  - Situation Helper에서 관련 앱이 2개 이상일때, 앱이 표시되지 않고 ValueError가 뜨던 현상 수정
  - 기존 코드가 Supabase와 맞지 않게 쉼표(,)로만 분리해, 파이프를 구분자로 인식하지 못하여 발생한 현상
- 관련 파일: 
  - `situation_helper.py`
  - `situation_helper.cpython-314.pyc`
- 비고:
  - 수정 후 정상적으로 추천 앱이 표시

  ---

## 1.6.07
- 날짜: 2026-07-16
- 변경자: codex (lemonlime-orange)
- 제목: introduction_to_travel_apps.html Added
- 요약: App Introduction .html file added+ Folder format changed
- 커밋 제목: introduction_to_travel_apps.html Added
- 변경 내용:
  - introduction_to_travel_apps.html 파일 새로 추가.
  - UPDATES.md와 함께 docs/ 폴더로 이동
- 관련 파일: 
  - `introduction_to_travel_apps.html`
  - `UPDATES.md`
  - `docs/`
- 비고:
  - README.md는 중요성을 고려해 docs/ 폴더로 이동 안함.