# Korea Travel Apps Guide (한국어)

Streamlit 기반 대한민국 여행자를 위한 앱 카탈로그 및 관리자 도구 모음

목표: 한국 방문객이 여행 중 유용한 앱을 빠르게 찾고 관리할 수 있도록 돕습니다.

---

## 핵심 변경사항 (이 업데이트)
- 문서 구조 정리: 설치·실행·기여 가이드 추가
- 데이터 스키마 및 폴더 구조 명확화
- 문제 해결(트러블슈팅)과 연락처 섹션 추가

---

## 목차

1. 프로젝트 개요
2. 주요 기능
3. 빠른 시작
4. 데이터 스키마
5. 폴더 구조
6. 관리자 접근
7. 기여 방법
8. 문제 해결
9. 라이선스 및 연락처

---

## 1) 프로젝트 개요

이 저장소는 한국 여행자를 위한 추천 모바일/웹 앱을 카테고리별로 보여주는 Streamlit 웹앱입니다. 앱 목록은 CSV로 관리되며, 관리자 UI로 앱을 추가·수정·삭제할 수 있습니다.

---

## 2) 주요 기능

- 카테고리별 앱 브라우징 (카테고리 복수 선택 가능, `|` 구분)
- 카테고리별 상단에 `Top Rated` 앱 강조
- 즐겨찾기(Favorites) 관리
- 상황별 추천 도우미(Situation Helper)
- 관리자 UI를 통해 앱 CRUD 지원

---

## 3) 빠른 시작

### 요구사항

- Python 3.9+ 권장
- `requirements.txt`에 필요한 패키지 목록 포함

### 설치

```bash
pip install -r requirements.txt
```

### 실행 (개발용)

```bash
streamlit run app.py
```

관리자 패널만 실행하려면:

```bash
streamlit run 9_🔧_Admin.py
```

브라우저 기본 주소: `http://localhost:8501`

---

## 4) 데이터 스키마 (`data/apps.csv`)

주요 컬럼(예시):

| 컬럼 | 설명 |
|------|------|
| id | 고유 ID (정수) |
| name | 앱 이름 |
| category | 카테고리(복수, `|` 구분) |
| icon | 이모지(옵션) |
| image_url | 로고/이미지 URL 또는 상대경로(옵션) |
| platform | 지원 플랫폼 (예: iOS, Android) |
| rating | 평점 (1.0–5.0) |
| download_url | 공식 URL |
| features | 주요 기능(여러 항목은 `|`로 구분) |
| tips | 간단 팁 |

참고: 관리자 UI는 현재 `image_url`을 텍스트로 받아 저장합니다. 파일 업로드 및 로컬 저장은 향후 구현 예정입니다.

---

## 5) 폴더 구조

```
travelapps/
├─ app.py                  # 메인 Streamlit 앱
├─ 9_🔧_Admin.py           # 관리자 패널 단독 실행용
├─ requirements.txt        # Python 의존성
├─ README.md               # 이 파일
├─ components/             # 재사용 UI 및 유틸
│  ├─ __init__.py
│  ├─ app_card.py          # 앱 카드 렌더링
│  ├─ data_loader.py       # CSV 읽기/쓰기 유틸
│  └─ admin_ui.py          # 관리자 UI 컴포넌트
├─ data/                   # CSV 데이터 저장소
│  ├─ apps.csv
│  ├─ favorites.csv
│  ├─ situations.csv
│  └─ emergency.csv
└─ assets/                 # 이미지·아이콘 등 정적 자원
	└─ images/
```

---

## 6) 관리자 접근

- 메인 앱 하단 `Administrator Controls`에서 관리자 UI를 임베드로 엽니다.
- 또는 터미널에서 `streamlit run 9_🔧_Admin.py`로 독립 실행하세요.

관리자 패널은 앱의 추가·수정·삭제 기능을 제공합니다. 접근 제어(비밀번호)는 `components/data_loader.py`에서 설정을 확인하세요.

---

## 7) 기여 방법

기여 환영합니다. 간단한 절차:

1. Fork 또는 브랜치 생성
2. 변경사항 구현 및 테스트
3. PR 생성 시 변경 요약과 테스트 방법 기재

코드 스타일: 기존 스타일을 따르세요. 주요 변경사항은 이슈로 먼저 제안해 주세요.

---

## 8) 문제 해결 (Troubleshooting)

- Streamlit이 포트 충돌로 실행되지 않으면 다른 포트로 실행하세요:

```bash
streamlit run app.py --server.port 8502
```

- CSV 파일이 비어 있거나 컬럼이 누락되면 `data/apps.csv` 샘플을 확인하세요.

문제점은 이 저장소의 이슈 트래커로 알려주세요.

---

## 9) 라이선스 및 연락처

문의/피드백: 저장소 이슈 또는 프로젝트 소유자에게 연락 바랍니다.
이메일: theonlylemon9@gmail.com

---

