"""
data_loader.py
CSV 파일에서 데이터를 불러오고 필터링하는 유틸리티 함수 모음
"""

import pandas as pd
import os
import json

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")


def _path(filename):
    return os.path.join(DATA_DIR, filename)


# ── 앱 데이터 ─────────────────────────────────────────────────

def load_apps() -> pd.DataFrame:
    df = pd.read_csv(_path("apps.csv"))
    if "icon" not in df.columns:
        df["icon"] = ""
    if "image_url" not in df.columns:
        df["image_url"] = ""
    return df

def get_categories(df: pd.DataFrame) -> list:
    categories = set()
    for value in df["category"].dropna().astype(str).tolist():
        for cat in value.split("|"):
            name = cat.strip()
            if name:
                categories.add(name)
    return sorted(categories)

def filter_by_category(df: pd.DataFrame, category: str) -> pd.DataFrame:
    if category == "All":
        return df
    return df[df["category"].astype(str).str.split("|").apply(
        lambda cats: category in [c.strip() for c in cats]
    )]

def search_apps(df: pd.DataFrame, query: str) -> pd.DataFrame:
    if not query:
        return df
    q = query.lower()
    mask = (
        df["name"].str.lower().str.contains(q) |
        df["description"].str.lower().str.contains(q) |
        df["category"].str.lower().str.contains(q)
    )
    return df[mask]

def get_apps_by_ids(df: pd.DataFrame, ids: list) -> pd.DataFrame:
    return df[df["id"].isin(ids)]

def get_top_rated_app(df: pd.DataFrame, category: str) -> dict:
    """카테고리별 최고 별점 앱 1개를 반환합니다."""
    cat_df = filter_by_category(df, category)
    if cat_df.empty:
        return None
    top = cat_df.nlargest(1, "rating").iloc[0]
    return top.to_dict()


# ── 즐겨찾기 ──────────────────────────────────────────────────

def load_favorites() -> list:
    df = pd.read_csv(_path("favorites.csv"))
    return df["app_id"].dropna().astype(int).tolist()

def save_favorites(app_ids: list):
    df = pd.DataFrame({"app_id": app_ids})
    df.to_csv(_path("favorites.csv"), index=False)

def is_favorite(app_id: int) -> bool:
    return app_id in load_favorites()

def toggle_favorite(app_id: int):
    favs = load_favorites()
    if app_id in favs:
        favs.remove(app_id)
    else:
        favs.append(app_id)
    save_favorites(favs)


# ── 관리자: 앱 CRUD ───────────────────────────────────────────

def save_apps(df: pd.DataFrame):
    """전체 앱 데이터프레임을 CSV에 저장합니다."""
    df.to_csv(_path("apps.csv"), index=False)

def add_app(new_app: dict) -> bool:
    """새 앱을 추가합니다. 성공 시 True 반환."""
    df = load_apps()
    new_id = int(df["id"].max()) + 1 if not df.empty else 1
    new_app["id"] = new_id
    new_row = pd.DataFrame([new_app])
    df = pd.concat([df, new_row], ignore_index=True)
    save_apps(df)
    return True

def update_app(app_id: int, updated: dict) -> bool:
    """기존 앱 정보를 수정합니다. 성공 시 True 반환."""
    df = load_apps()
    idx = df.index[df["id"] == app_id]
    if idx.empty:
        return False
    for key, val in updated.items():
        df.at[idx[0], key] = val
    save_apps(df)
    return True

def delete_app(app_id: int) -> bool:
    """앱을 삭제합니다. 성공 시 True 반환."""
    df = load_apps()
    if app_id not in df["id"].values:
        return False
    df = df[df["id"] != app_id].reset_index(drop=True)
    save_apps(df)
    # 즐겨찾기에서도 제거
    favs = load_favorites()
    if app_id in favs:
        favs.remove(app_id)
        save_favorites(favs)
    return True


# ── 관리자: 비밀번호 확인 ──────────────────────────────────────

ADMIN_PASSWORD = "admin1234"  # 실제 배포 시 환경변수로 교체 권장

def check_password(pw: str) -> bool:
    return pw == ADMIN_PASSWORD


# ── 상황 데이터 ───────────────────────────────────────────────

def load_situations() -> pd.DataFrame:
    return pd.read_csv(_path("situations.csv"))

def save_situations(df: pd.DataFrame):
    """전체 상황 데이터프레임을 CSV에 저장합니다."""
    df.to_csv(_path("situations.csv"), index=False)

def get_situation_categories() -> list:
    """모든 상황 카테고리를 반환합니다. 기본 카테고리를 보장합니다."""
    df = load_situations()
    found = []
    if not df.empty:
        found = [c for c in df["category"].dropna().astype(str).unique().tolist()]

    defaults = [
        "Navigation/Tourism Problems",
        "Translation Problems",
        "Delivery Problems",
        "Money Problems",
        "Hotel Problems",
        "Travel Problems",
        "Other Problems",
    ]

    # Merge defaults and found categories while preserving defaults order and avoiding duplicates
    categories = []
    for d in defaults:
        if d not in categories:
            categories.append(d)
    for c in found:
        if c and c not in categories:
            categories.append(c)

    return categories

def load_situations_by_category(category: str) -> pd.DataFrame:
    """특정 카테고리의 상황들을 반환합니다."""
    df = load_situations()
    if category == "All":
        return df
    return df[df["category"] == category]

def add_situation(new_situation: dict) -> bool:
    """새 상황을 추가합니다. 성공 시 True 반환."""
    df = load_situations()
    new_id = int(df["id"].max()) + 1 if not df.empty else 1
    new_situation["id"] = new_id
    new_row = pd.DataFrame([new_situation])
    df = pd.concat([df, new_row], ignore_index=True)
    save_situations(df)
    return True

def update_situation(situation_id: int, updated: dict) -> bool:
    """기존 상황 정보를 수정합니다. 성공 시 True 반환."""
    df = load_situations()
    idx = df.index[df["id"] == situation_id]
    if idx.empty:
        return False
    for key, val in updated.items():
        df.at[idx[0], key] = val
    save_situations(df)
    return True

def delete_situation(situation_id: int) -> bool:
    """상황을 삭제합니다. 성공 시 True 반환."""
    df = load_situations()
    if situation_id not in df["id"].values:
        return False
    df = df[df["id"] != situation_id].reset_index(drop=True)
    save_situations(df)
    return True


# ── 응급 데이터 ───────────────────────────────────────────────

def load_emergency() -> pd.DataFrame:
    return pd.read_csv(_path("emergency.csv"))


# ── 사이트 설정 저장소 (간단한 JSON 파일) ─────────────────────────
SETTINGS_FILENAME = "settings.json"


def load_settings() -> dict:
    """설정 JSON을 로드합니다. 파일이 없거나 파싱 실패 시 빈 dict 반환."""
    p = _path(SETTINGS_FILENAME)
    if not os.path.exists(p):
        return {}
    try:
        with open(p, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def save_settings(settings: dict):
    """설정 dict을 JSON 파일로 저장합니다."""
    p = _path(SETTINGS_FILENAME)
    with open(p, "w", encoding="utf-8") as f:
        json.dump(settings, f, ensure_ascii=False, indent=2)


def get_before_land_tips() -> list:
    """'Before You Land' 팁 목록을 문자열 리스트로 반환합니다."""
    settings = load_settings()
    tips = settings.get("before_land", [])
    # 보수적으로 None 또는 단일 문자열을 처리
    if isinstance(tips, str):
        return [tips]
    if not isinstance(tips, list):
        return []
    return tips


def update_before_land_tips(tips: list) -> bool:
    """새 팁 목록으로 업데이트 후 저장합니다."""
    settings = load_settings()
    settings["before_land"] = tips
    save_settings(settings)
    return True
