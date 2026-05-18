"""
data_loader.py
CSV 파일에서 앱 데이터를 불러오는 유틸리티 함수들
"""

import pandas as pd
import os

# CSV 파일 경로 (data_loader.py 기준 상대 경로)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV_PATH = os.path.join(BASE_DIR, "data", "apps.csv")


def load_apps() -> pd.DataFrame:
    """CSV 파일에서 앱 목록을 불러옵니다."""
    df = pd.read_csv(CSV_PATH)
    return df


def get_categories(df: pd.DataFrame) -> list:
    """앱 카테고리 목록을 반환합니다."""
    return sorted(df["category"].unique().tolist())


def filter_by_category(df: pd.DataFrame, category: str) -> pd.DataFrame:
    """특정 카테고리의 앱만 필터링합니다."""
    if category == "All":
        return df
    return df[df["category"] == category]


def search_apps(df: pd.DataFrame, query: str) -> pd.DataFrame:
    """앱 이름 또는 설명에서 키워드를 검색합니다."""
    if not query:
        return df
    query = query.lower()
    mask = (
        df["name"].str.lower().str.contains(query) |
        df["description"].str.lower().str.contains(query) |
        df["category"].str.lower().str.contains(query)
    )
    return df[mask]


def get_app_by_id(df: pd.DataFrame, app_id: int) -> pd.Series | None:
    """ID로 특정 앱 정보를 가져옵니다."""
    result = df[df["id"] == app_id]
    if result.empty:
        return None
    return result.iloc[0]
