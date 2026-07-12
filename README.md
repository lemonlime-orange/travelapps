# Korea Travel Apps Guide

한국 방문자가 상황과 주제에 맞는 필수 여행 앱을 빠르게 찾을 수 있도록 만든 Streamlit 기반 웹 앱입니다. 앱 정보와 사용자 데이터는 Supabase에 저장하며, 관리자는 별도의 관리 화면에서 앱과 추천 정보를 관리할 수 있습니다.

## 주요 기능

- 주제별 여행 앱 탐색
- 개발자가 직접 테스트 해 추천하는 `Essential Apps`
- 상황별 앱/대응 방안을 안내하는 `Situation Helper`
- 앱 상세 정보, 개발사, 주요 기능, 팁, 스토어 링크 등 제공
- 사용 방법 이미지와 In-App 이미지 갤러리
- 회원가입 및 로그인 기능
- 로그인 사용자별 Favorites와 Downloaded Apps 저장
- 다운로드한 앱에 대한 별점 및 리뷰 작성
- 관리자 화면에서 앱, Essential Apps, 상황별 추천, 리뷰 및 안내 문구 관리

## 기술 스택

- Python 3.9+
- Streamlit
- pandas
- Supabase (Database, Storage)
- bcrypt

## 설치 및 실행

### 1. 저장소와 가상환경 준비

```bash
python -m venv .venv
```

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

### 2. 패키지 설치

```bash
pip install -r requirements.txt
```

### 3. Supabase 설정

Supabase SQL Editor에서 [`supabase_apps_schema.sql`](supabase_apps_schema.sql)을 실행해 필요한 테이블과 정책을 생성합니다.

그다음 `.streamlit/secrets.example.toml`을 참고하여 `.streamlit/secrets.toml`을 만듭니다.

```toml
SUPABASE_URL = "https://your-project.supabase.co"
SUPABASE_ANON_KEY = "your-anon-key"
SUPABASE_SERVICE_ROLE_KEY = "your-service-role-key"
SUPABASE_BUCKET = "internal-assets"
```

`SUPABASE_SERVICE_ROLE_KEY`는 관리자 작업에 사용되므로 Git에 커밋하거나 외부에 공개하지 마세요. 이미지 업로드를 사용하려면 `SUPABASE_BUCKET`에 지정한 Storage 버킷도 준비해야 합니다.

### 4. 앱 실행

```bash
streamlit run app.py
```

기본 주소는 `http://localhost:8501`입니다. 포트가 사용 중이면 다음처럼 다른 포트를 지정할 수 있습니다.

```bash
streamlit run app.py --server.port 8502
```

관리자 진입용 파일을 직접 실행할 수도 있습니다.

```bash
streamlit run 9_🔧_Admin.py
```

## 사용 방법

홈 화면에서 Essential Apps 또는 원하는 주제를 선택해 앱을 탐색합니다. 앱 상세 화면에서는 스토어 링크, 기능, 팁, 가이드 이미지와 앱 내부 이미지를 확인할 수 있습니다.

Favorites와 Downloaded Apps는 로그인한 사용자만 이용할 수 있습니다. 리뷰는 로그인 후 해당 앱을 Downloaded Apps에 추가한 사용자만 작성할 수 있습니다.

## 관리자 기능

사이드바의 `Administrator Controls`에서 관리자 화면을 열 수 있습니다. 관리자 권한 확인 후 다음 기능을 사용할 수 있습니다.

- 앱 추가, 수정 및 삭제
- 앱 아이콘, 가이드 이미지, In-App 이미지 업로드
- Essential Apps 지정 및 해제
- Situation Helper 항목 관리
- 리뷰 조회 및 삭제
- `Before You Land in Korea` 안내 문구 관리

Essential Apps는 일반 카테고리 문자열에 포함되지 않으며 Supabase의 `essential_apps` 테이블에서 `app_id` 기준으로 별도 관리됩니다.

## 주요 데이터 구조

### `apps`

| 필드 | 설명 |
|---|---|
| `id` | 앱 고유 ID |
| `name` | 앱 이름 |
| `category` | 일반 카테고리. 여러 값은 `\|`로 구분 |
| `developer` | 개발사 |
| `description` | 앱 설명 |
| `platform` | 지원 플랫폼 |
| `rating` | 기본 평점 |
| `downloads` | 다운로드 정보 |
| `features` | 주요 기능. 여러 값은 `\|`로 구분 |
| `tips` | 사용 팁 |
| `app icon` / `image_url` | 아이콘 또는 대표 이미지 |
| `app_store_url` | Apple App Store URL |
| `play_store_url` | Google Play Store URL |
| `guide_images` | 사용 가이드 이미지 목록 |
| `guide_image_captions` | 사용 가이드 이미지 설명 |
| `in_app_images` | 앱 내부 이미지 목록 |
| `in_app_image_captions` | 앱 내부 이미지 설명 |

이미지와 캡션을 여러 개 저장할 때는 같은 순서로 `|` 구분자를 사용합니다.

### 기타 주요 테이블

| 테이블 | 용도 |
|---|---|
| `essential_apps` | Essential Apps로 선택된 앱 ID |
| `situations` | 상황별 설명 및 추천 앱 |
| `app_users` | 사용자 계정 |
| `user_favorites` | 사용자별 즐겨찾기 |
| `user_downloads` | 사용자별 다운로드 앱 |
| `app_reviews` | 사용자 별점 및 리뷰 |

정확한 최신 스키마는 [`supabase_apps_schema.sql`](supabase_apps_schema.sql)을 기준으로 확인하세요.

## 기존 CSV 데이터 이전

`scripts/` 디렉터리에는 기존 로컬 데이터를 Supabase로 이전하기 위한 스크립트가 있습니다.

- `migrate_apps_to_supabase.py`: 앱 데이터 이전
- `migrate_admin_data_to_supabase.py`: 관리자 데이터 이전
- `migrate_user_data_to_supabase.py`: 사용자, Favorites, Downloaded Apps, 리뷰 이전

실행 전 `.streamlit/secrets.toml` 설정과 대상 Supabase 프로젝트를 반드시 확인하세요.

## 프로젝트 구조

```text
travelapps/
├── app.py
├── 9_🔧_Admin.py
├── components/
│   ├── admin_ui.py
│   ├── app_card.py
│   ├── data_loader.py
│   ├── sidebar.py
│   └── situation_helper.py
├── data/
├── assets/
│   ├── fonts/
│   └── images/
├── scripts/
├── .streamlit/
│   └── secrets.example.toml
├── requirements.txt
├── supabase_apps_schema.sql
├── UPDATES.md
└── README.md
```

## 문제 해결

- `Missing Supabase settings` 오류가 표시되면 `.streamlit/secrets.toml`의 URL과 키 이름을 확인하세요.
- 앱 메타데이터 컬럼 오류가 발생하면 최신 `supabase_apps_schema.sql`을 다시 적용하세요.
- 이미지 업로드가 실패하면 Storage 버킷 이름과 서비스 역할 키를 확인하세요.
- 로그인 또는 비밀번호 처리 오류가 발생하면 현재 가상환경에 `bcrypt`가 설치되어 있는지 확인하세요.

## 기여 방법

1. 새 브랜치를 만듭니다.
2. 변경사항을 구현하고 로컬에서 실행해 확인합니다.
3. 비밀 키, 사용자 데이터, 캐시 파일이 커밋에 포함되지 않았는지 확인합니다.
4. 변경 목적과 테스트 방법을 적어 Pull Request를 생성합니다.

변경 내역은 [`UPDATES.md`](UPDATES.md)에서 확인할 수 있습니다.

## 문의

문의/피드백: 프로젝트 소유자에게 연락 바랍니다.
이메일: theonlylemon9@gmail.com
