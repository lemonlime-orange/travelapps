# 🇰🇷 Korea Travel Apps Guide

Streamlit 기반 대한민국 여행자를 위한 필수 앱 가이드 웹앱

---

## 프로젝트 개요

이 프로젝트는 한국 방문자를 위한 추천 앱을 카테고리별로 보여주는 Streamlit 웹앱입니다. 앱 목록은 CSV로 관리되며, 관리자 UI로 앱을 추가·수정·삭제할 수 있습니다.

---

## 주요 기능

- 카테고리별 앱 브라우징 (멀티 카테고리 태그 지원 — `|`로 구분된 값 사용)
- 각 카테고리 상단에 **🌟 Top Rated App** 자동 표시
- 즐겨찾기(Favorites) 목록 지원
- 사이트 하단의 `Administrator Controls`를 통해 관리자 패널 접근(또는 `9_🔧_Admin.py` 단독 실행 가능)
- 앱 데이터는 `data/apps.csv`로 관리

---

## 폴더 구조

```
travelapps/
├─ app.py                  # 메인 Streamlit 앱
├─ 9_🔧_Admin.py           # 관리자 페이지(단독 실행 가능)
├─ requirements.txt        # Python 의존성
├─ README.md               # 이 파일
├─ components/             # 재사용 가능한 UI·유틸 컴포넌트
│  ├─ __init__.py
│  ├─ app_card.py          # 앱 카드 렌더링
│  ├─ data_loader.py       # CSV 읽기/쓰기, 필터링, 유틸 함수
│  └─ admin_ui.py          # 임베드 가능한 관리자 패널 구현
├─ data/                   # 데이터 저장소
│  ├─ apps.csv             # 앱 목록(저장 및 로드 대상)
│  ├─ favorites.csv        # 사용자 즐겨찾기 저장
│  ├─ situations.csv       # 상황별 추천 매핑(사용처에 따라)
│  └─ emergency.csv        # 비상 연락처 등
└─ pages/ (optional)       # 향후 다중 페이지 구성에 사용 가능
```

---

## 실행 방법

1) 의존성 설치

```bash
pip install -r requirements.txt
```

2) 로컬에서 앱 실행

```bash
streamlit run app.py
```

3) 관리자 패널만 실행하려면

```bash
streamlit run 9_🔧_Admin.py
```

브라우저에서 보통 `http://localhost:8501`로 접속합니다.

---

## 데이터 스키마 (`data/apps.csv`)

CSV의 주요 컬럼은 다음과 같습니다. `category`와 `features`는 파이프(`|`)로 여러 값을 연결해 사용합니다.

| 컬럼 | 설명 |
|------|------|
| id | 고유 ID (정수)
| name | 앱 이름
| category | 카테고리(복수 선택 가능, `|`로 구분)
| icon | 이모지 아이콘(옵션)
| image_url | 앱 로고 또는 이미지 경로/URL(옵션)
| platform | 지원 플랫폼 (예: `iOS, Android`)
| rating | 평점 (1.0–5.0)
| download_url | 공식 다운로드/정보 URL
| features | 주요 기능(줄바꿈 대신 `|`로 구분)
| tips | 앱 사용 팁

주의: 현재 관리자 UI는 `image_url` 텍스트 입력을 통해 외부 URL이나 프로젝트 내 경로를 저장합니다. 파일 업로드(로컬로 저장)는 추후 구현 예정입니다.

---

## 관리자 접근

- 메인 페이지 하단의 `Administrator Controls`를 열고 `Open Admin Panel` 버튼을 누르면 관리자 UI를 임베드하여 사용 가능합니다.
- 또는 터미널에서 `streamlit run 9_🔧_Admin.py`로 독립 실행할 수 있습니다.

관리자 패널에서는 앱 추가·수정·삭제 기능을 제공합니다. 기본적인 접근 제어(비밀번호 확인)가 포함되어 있으니 비밀번호는 `components/data_loader.py`의 설정을 확인하세요.

---

## 알려진 TODO

- 이미지 파일 업로드(파일 업로드 → 프로젝트 폴더 저장) 기능 추가
- 관리자 접근 권한 강화(사용자 계정/암호 관리)
- 앱 상세 페이지와 통계 대시보드 추가
- 다국어(한국어/영어) UI 개선

---

원하시면 README에 설치 스크린샷이나 운영 예시(예: Docker)도 추가해 드리겠습니다.
