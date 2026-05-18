# 🇰🇷 Korea Travel Apps Guide

외국인 여행자를 위한 대한민국 필수 앱 추천 웹앱 (Streamlit 기반)

---

## 📁 폴더 구조

```
korea_travel_app/
│
├── app.py                  ← 메인 진입점 (여기서 실행!)
├── requirements.txt        ← 필요한 라이브러리 목록
├── README.md               ← 이 파일
│
├── data/
│   └── apps.csv            ← 앱 데이터 저장소 (직접 수정 가능)
│
└── components/
    ├── data_loader.py      ← CSV 읽기 / 필터링 / 검색 함수
    ├── app_card.py         ← 앱 카드 UI 컴포넌트
    └── sidebar.py          ← 사이드바 필터 UI 컴포넌트
```

---

## 🚀 실행 방법

```bash
# 1. 의존성 설치
pip install -r requirements.txt

# 2. 앱 실행
streamlit run app.py
```

브라우저에서 `http://localhost:8501` 이 자동으로 열립니다.

---

## 📊 데이터 수정 방법

`data/apps.csv` 파일을 Excel이나 텍스트 편집기로 열어 직접 수정할 수 있습니다.

| 컬럼 | 설명 | 예시 |
|------|------|------|
| id | 고유 번호 | 1 |
| name | 앱 이름 | Naver Maps |
| category | 카테고리 | Navigation |
| icon | 이모지 아이콘 | 🗺️ |
| description | 앱 설명 | The most accurate... |
| platform | 지원 플랫폼 | iOS, Android |
| rating | 평점 (5점 만점) | 4.8 |
| download_url | 공식 사이트 URL | https://... |
| features | 주요 기능 (`\|`로 구분) | Route planning\|Offline maps |
| tips | 여행 팁 | Switch to English in settings |

---

## 🛠️ 앞으로 추가할 수 있는 기능

- [ ] 앱 상세 페이지 (pages/ 폴더 활용)
- [ ] 즐겨찾기 기능
- [ ] 카테고리별 통계 차트
- [ ] 사용자 리뷰 입력
- [ ] 다국어 지원 (한국어/영어/일본어/중국어)
