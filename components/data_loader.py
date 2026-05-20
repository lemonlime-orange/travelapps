"""
data_loader.py
CSV 파일에서 데이터를 불러오고 필터링하는 유틸리티 함수 모음
"""

import pandas as pd
import os

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


# ── 응급 데이터 ───────────────────────────────────────────────

def load_emergency() -> pd.DataFrame:
    return pd.read_csv(_path("emergency.csv"))
