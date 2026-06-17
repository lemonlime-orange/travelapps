import json
import mimetypes
import os
import uuid
from datetime import datetime

import pandas as pd

try:
    import streamlit as st
except Exception:
    st = None

try:
    from supabase import create_client
except Exception:
    create_client = None


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")

APPS_TABLE = "apps"
SITUATIONS_TABLE = "situations"
SETTINGS_TABLE = "app_settings"
STORE_URL_COLUMNS = ("app_store_url", "play_store_url")
APP_SCHEMA_COLUMNS = STORE_URL_COLUMNS + ("in_app_images", "in_app_image_captions")
APP_COLUMNS = [
    "id",
    "name",
    "category",
    "icon",
    "description",
    "platform",
    "rating",
    "app_store_url",
    "play_store_url",
    "features",
    "tips",
    "image_url",
    "in_app_images",
    "in_app_image_captions",
    "guide_images",
    "guide_image_captions",
]
SITUATION_COLUMNS = [
    "id",
    "situation",
    "emoji",
    "description",
    "category",
    "app_ids",
]

ADMIN_PASSWORD = "travel2korea"
SETTINGS_FILENAME = "settings.json"
SUPABASE_PAGE_SIZE = 1000
REVIEWS_FILENAME = "app_reviews.csv"
MIN_REVIEWS_FOR_AVERAGE_RATING = 5
REVIEW_COLUMNS = [
    "user_id",
    "username",
    "app_id",
    "rating",
    "review",
    "used_after_download",
    "created_at",
    "updated_at",
]


def _path(filename):
    return os.path.join(DATA_DIR, filename)


def _secret(name, default=""):
    value = os.environ.get(name)
    if value:
        return value
    if st is not None:
        try:
            return st.secrets.get(name, default)
        except Exception:
            return default
    return default


def _notify_error(message):
    if st is not None:
        try:
            st.error(message)
            return
        except Exception:
            pass
    print(message)


def get_supabase_bucket():
    return _secret("SUPABASE_BUCKET", "internal-assets")


def get_supabase_client(use_service_role=False):
    if create_client is None:
        raise RuntimeError("The 'supabase' package is not installed. Run: pip install -r requirements.txt")

    url = _secret("SUPABASE_URL")
    key_name = "SUPABASE_SERVICE_ROLE_KEY" if use_service_role else "SUPABASE_ANON_KEY"
    key = _secret(key_name)
    if not url or not key:
        raise RuntimeError(
            f"Missing Supabase settings. Add SUPABASE_URL and {key_name} to .streamlit/secrets.toml."
        )
    return create_client(url, key)


def _empty_apps_df():
    return pd.DataFrame(columns=APP_COLUMNS)


def _empty_situations_df():
    return pd.DataFrame(columns=SITUATION_COLUMNS)


def _select_all_rows(client, table_name, columns, order_column="id"):
    rows = []
    start = 0

    while True:
        end = start + SUPABASE_PAGE_SIZE - 1
        response = (
            client.table(table_name)
            .select(",".join(columns))
            .order(order_column)
            .range(start, end)
            .execute()
        )
        batch = response.data or []
        rows.extend(batch)

        if len(batch) < SUPABASE_PAGE_SIZE:
            break
        start += SUPABASE_PAGE_SIZE

    return rows


def _normalize_apps_df(df):
    for col in APP_COLUMNS:
        if col not in df.columns:
            df[col] = 0 if col == "rating" else ""
    if not df.empty:
        df["id"] = pd.to_numeric(df["id"], errors="coerce").fillna(0).astype(int)
        df["rating"] = pd.to_numeric(df["rating"], errors="coerce").fillna(0.0)
        for col in APP_COLUMNS:
            if col not in ("id", "rating"):
                df[col] = df[col].fillna("").astype(str)
    return df[APP_COLUMNS]


def _schema_missing_store_url_columns(exc):
    message = str(exc).lower()
    return any(col in message for col in APP_SCHEMA_COLUMNS)


def _store_url_schema_message(exc):
    if _schema_missing_store_url_columns(exc):
        return (
            "Supabase apps table is missing one or more app metadata columns. "
            "Run the ALTER TABLE section in supabase_apps_schema.sql first."
        )
    return str(exc)


def _normalize_situations_df(df):
    for col in SITUATION_COLUMNS:
        if col not in df.columns:
            df[col] = 0 if col == "id" else ""
    if not df.empty:
        df["id"] = pd.to_numeric(df["id"], errors="coerce").fillna(0).astype(int)
        for col in SITUATION_COLUMNS:
            if col != "id":
                df[col] = df[col].fillna("").astype(str)
    return df[SITUATION_COLUMNS]


def _app_payload(app):
    payload = {}
    for col in APP_COLUMNS:
        value = app.get(col, 0 if col in ("id", "rating") else "")
        if col == "id":
            value = int(value)
        elif col == "rating":
            value = float(value or 0)
        else:
            value = "" if value is None else str(value)
        payload[col] = value
    return payload


def _situation_payload(situation):
    payload = {}
    for col in SITUATION_COLUMNS:
        value = situation.get(col, 0 if col == "id" else "")
        if col == "id":
            value = int(value)
        else:
            value = "" if value is None else str(value)
        payload[col] = value
    return payload


def load_apps(use_service_role=False):
    try:
        client = get_supabase_client(use_service_role=use_service_role)
        rows = _select_all_rows(client, APPS_TABLE, APP_COLUMNS)
        return _normalize_apps_df(pd.DataFrame(rows))
    except Exception as exc:
        _notify_error(f"Supabase app data could not be loaded: {exc}")
        return _empty_apps_df()


def save_apps(df):
    try:
        client = get_supabase_client(use_service_role=True)
        rows = [_app_payload(row) for row in _normalize_apps_df(df).to_dict("records")]
        client.table(APPS_TABLE).delete().neq("id", -1).execute()
        if rows:
            client.table(APPS_TABLE).upsert(rows, on_conflict="id").execute()
        return True
    except Exception as exc:
        _notify_error(f"Supabase app data could not be saved: {_store_url_schema_message(exc)}")
        return False


def add_app(new_app):
    try:
        df = load_apps(use_service_role=True)
        new_id = int(df["id"].max()) + 1 if not df.empty else 1
        new_app["id"] = new_id
        client = get_supabase_client(use_service_role=True)
        client.table(APPS_TABLE).insert(_app_payload(new_app)).execute()
        return True
    except Exception as exc:
        _notify_error(f"Supabase app could not be added: {_store_url_schema_message(exc)}")
        return False


def update_app(app_id, updated):
    try:
        payload = {key: value for key, value in updated.items() if key in APP_COLUMNS and key != "id"}
        if "rating" in payload:
            payload["rating"] = float(payload.get("rating") or 0)
        for key in list(payload.keys()):
            if key != "rating":
                payload[key] = "" if payload[key] is None else str(payload[key])
        client = get_supabase_client(use_service_role=True)
        client.table(APPS_TABLE).update(payload).eq("id", int(app_id)).execute()
        return True
    except Exception as exc:
        _notify_error(f"Supabase app could not be updated: {_store_url_schema_message(exc)}")
        return False


def delete_app(app_id):
    try:
        client = get_supabase_client(use_service_role=True)
        client.table(APPS_TABLE).delete().eq("id", int(app_id)).execute()
        favs = load_favorites()
        if app_id in favs:
            favs.remove(app_id)
            save_favorites(favs)
        return True
    except Exception as exc:
        _notify_error(f"Supabase app could not be deleted: {exc}")
        return False


def upload_internal_asset(uploaded_file, folder="guide-images"):
    client = get_supabase_client(use_service_role=True)
    bucket = get_supabase_bucket()
    original_name = os.path.basename(uploaded_file.name)
    safe_name = f"{uuid.uuid4().hex}_{original_name}"
    storage_path = f"{folder.strip('/')}/{safe_name}"
    content_type = uploaded_file.type or mimetypes.guess_type(original_name)[0] or "application/octet-stream"
    client.storage.from_(bucket).upload(
        path=storage_path,
        file=uploaded_file.getvalue(),
        file_options={"content-type": content_type, "upsert": False},
    )
    return client.storage.from_(bucket).get_public_url(storage_path)


def get_categories(df):
    categories = set()
    for value in df["category"].dropna().astype(str).tolist():
        for cat in value.split("|"):
            name = cat.strip()
            if name:
                categories.add(name)
    return sorted(categories)


def filter_by_category(df, category):
    if category == "All":
        return df
    return df[df["category"].astype(str).str.split("|").apply(
        lambda cats: category in [c.strip() for c in cats]
    )]


def search_apps(df, query):
    if not query:
        return df
    q = query.lower()
    mask = (
        df["name"].str.lower().str.contains(q) |
        df["description"].str.lower().str.contains(q) |
        df["category"].str.lower().str.contains(q)
    )
    return df[mask]


def get_apps_by_ids(df, ids):
    return df[df["id"].isin(ids)]


def get_top_rated_app(df, category):
    cat_df = filter_by_category(df, category)
    if cat_df.empty:
        return None
    cat_df = cat_df.copy()
    cat_df["display_rating"] = cat_df.apply(
        lambda row: get_display_rating(row["id"], row["rating"])[0],
        axis=1,
    )
    top = cat_df.nlargest(1, "display_rating").iloc[0]
    return top.to_dict()


def load_favorites():
    df = pd.read_csv(_path("favorites.csv"))
    return df["app_id"].dropna().astype(int).tolist()


def save_favorites(app_ids):
    df = pd.DataFrame({"app_id": app_ids})
    df.to_csv(_path("favorites.csv"), index=False)


def is_favorite(app_id):
    return app_id in load_favorites()


def toggle_favorite(app_id):
    favs = load_favorites()
    if app_id in favs:
        favs.remove(app_id)
    else:
        favs.append(app_id)
    save_favorites(favs)


def load_downloads():
    p = _path("downloads.csv")
    if not os.path.exists(p):
        return []
    df = pd.read_csv(p)
    if "app_id" not in df.columns:
        return []
    return df["app_id"].dropna().astype(int).tolist()


def save_downloads(app_ids):
    df = pd.DataFrame({"app_id": app_ids})
    df.to_csv(_path("downloads.csv"), index=False)


def is_downloaded(app_id):
    return app_id in load_downloads()


def toggle_downloaded(app_id):
    dl = load_downloads()
    if app_id in dl:
        dl.remove(app_id)
    else:
        dl.append(app_id)
    save_downloads(dl)


def _empty_reviews_df():
    return pd.DataFrame(columns=REVIEW_COLUMNS)


def _normalize_reviews_df(df):
    for col in REVIEW_COLUMNS:
        if col not in df.columns:
            df[col] = ""
    if not df.empty:
        df["app_id"] = pd.to_numeric(df["app_id"], errors="coerce").fillna(0).astype(int)
        df["rating"] = pd.to_numeric(df["rating"], errors="coerce").fillna(0.0)
        df["used_after_download"] = df["used_after_download"].astype(str).str.lower().isin(
            ["true", "1", "yes", "y"]
        )
        for col in REVIEW_COLUMNS:
            if col not in ("app_id", "rating", "used_after_download"):
                df[col] = df[col].fillna("").astype(str)
    return df[REVIEW_COLUMNS]


def load_reviews():
    p = _path(REVIEWS_FILENAME)
    if not os.path.exists(p):
        return _empty_reviews_df()
    try:
        return _normalize_reviews_df(pd.read_csv(p))
    except Exception:
        return _empty_reviews_df()


def save_reviews(df):
    normalized = _normalize_reviews_df(df)
    normalized.to_csv(_path(REVIEWS_FILENAME), index=False)


def get_app_reviews(app_id):
    reviews = load_reviews()
    if reviews.empty:
        return reviews
    return reviews[reviews["app_id"] == int(app_id)].sort_values("updated_at", ascending=False)


def get_user_app_review(app_id, user_id):
    reviews = get_app_reviews(app_id)
    if reviews.empty:
        return None
    user_reviews = reviews[reviews["user_id"].astype(str) == str(user_id)]
    if user_reviews.empty:
        return None
    return user_reviews.iloc[0].to_dict()


def upsert_app_review(app_id, user_id, username, rating, review, used_after_download=True):
    reviews = load_reviews()
    now = datetime.utcnow().isoformat() + "Z"
    user_id = str(user_id)
    app_id = int(app_id)
    rating = max(0.0, min(5.0, round(float(rating or 0) * 2) / 2))
    mask = (reviews["app_id"] == app_id) & (reviews["user_id"].astype(str) == user_id)

    row = {
        "user_id": user_id,
        "username": str(username or "Traveler"),
        "app_id": app_id,
        "rating": rating,
        "review": str(review or "").strip(),
        "used_after_download": bool(used_after_download),
        "created_at": now,
        "updated_at": now,
    }

    if mask.any():
        first_index = reviews[mask].index[0]
        row["created_at"] = reviews.at[first_index, "created_at"] or now
        for key, value in row.items():
            reviews.at[first_index, key] = value
    else:
        reviews = pd.concat([reviews, pd.DataFrame([row])], ignore_index=True)

    save_reviews(reviews)


def delete_app_review(app_id, user_id):
    reviews = load_reviews()
    if reviews.empty:
        return
    mask = (reviews["app_id"] == int(app_id)) & (reviews["user_id"].astype(str) == str(user_id))
    save_reviews(reviews[~mask].reset_index(drop=True))


def get_app_review_summary(app_id):
    reviews = get_app_reviews(app_id)
    if reviews.empty:
        return 0.0, 0
    return float(reviews["rating"].mean()), int(len(reviews))


def _round_rating_for_display(value):
    return int(float(value or 0) * 10 + 0.5) / 10


def get_display_rating(app_id, fallback_rating):
    avg_rating, review_count = get_app_review_summary(app_id)
    if review_count >= MIN_REVIEWS_FOR_AVERAGE_RATING:
        return _round_rating_for_display(avg_rating), review_count, "reviews"
    return _round_rating_for_display(fallback_rating), review_count, "admin"


def check_password(pw):
    return pw == ADMIN_PASSWORD


def load_situations():
    try:
        client = get_supabase_client()
        response = client.table(SITUATIONS_TABLE).select(",".join(SITUATION_COLUMNS)).order("id").execute()
        return _normalize_situations_df(pd.DataFrame(response.data or []))
    except Exception as exc:
        _notify_error(f"Supabase situation data could not be loaded; using local CSV: {exc}")
        p = _path("situations.csv")
        if not os.path.exists(p):
            return _empty_situations_df()
        return _normalize_situations_df(pd.read_csv(p))


def save_situations(df):
    normalized = _normalize_situations_df(df)
    try:
        client = get_supabase_client(use_service_role=True)
        rows = [_situation_payload(row) for row in normalized.to_dict("records")]
        client.table(SITUATIONS_TABLE).delete().neq("id", -1).execute()
        if rows:
            client.table(SITUATIONS_TABLE).upsert(rows, on_conflict="id").execute()
        return True
    except Exception as exc:
        _notify_error(f"Supabase situation data could not be saved; using local CSV: {exc}")
        normalized.to_csv(_path("situations.csv"), index=False)
        return False


def get_situation_categories():
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

    categories = []
    for item in defaults + found:
        if item and item not in categories:
            categories.append(item)
    return categories


def load_situations_by_category(category):
    df = load_situations()
    if category == "All":
        return df
    return df[df["category"] == category]


def add_situation(new_situation):
    try:
        df = load_situations()
        new_id = int(df["id"].max()) + 1 if not df.empty else 1
        new_situation["id"] = new_id
        client = get_supabase_client(use_service_role=True)
        client.table(SITUATIONS_TABLE).insert(_situation_payload(new_situation)).execute()
        return True
    except Exception as exc:
        _notify_error(f"Supabase situation could not be added; using local CSV: {exc}")
        df = load_situations()
        new_id = int(df["id"].max()) + 1 if not df.empty else 1
        new_situation["id"] = new_id
        new_row = pd.DataFrame([new_situation])
        df = pd.concat([df, new_row], ignore_index=True)
        df.to_csv(_path("situations.csv"), index=False)
        return False


def update_situation(situation_id, updated):
    try:
        payload = {key: value for key, value in updated.items() if key in SITUATION_COLUMNS and key != "id"}
        payload = {key: "" if value is None else str(value) for key, value in payload.items()}
        client = get_supabase_client(use_service_role=True)
        client.table(SITUATIONS_TABLE).update(payload).eq("id", int(situation_id)).execute()
        return True
    except Exception as exc:
        _notify_error(f"Supabase situation could not be updated; using local CSV: {exc}")
        df = load_situations()
        idx = df.index[df["id"] == int(situation_id)]
        if idx.empty:
            return False
        for key, val in updated.items():
            df.at[idx[0], key] = val
        df.to_csv(_path("situations.csv"), index=False)
        return False


def delete_situation(situation_id):
    try:
        client = get_supabase_client(use_service_role=True)
        client.table(SITUATIONS_TABLE).delete().eq("id", int(situation_id)).execute()
        return True
    except Exception as exc:
        _notify_error(f"Supabase situation could not be deleted; using local CSV: {exc}")
        df = load_situations()
        situation_id = int(situation_id)
        if situation_id not in df["id"].values:
            return False
        df = df[df["id"] != situation_id].reset_index(drop=True)
        df.to_csv(_path("situations.csv"), index=False)
        return False


def load_emergency():
    return pd.read_csv(_path("emergency.csv"))


def load_settings():
    try:
        client = get_supabase_client()
        response = client.table(SETTINGS_TABLE).select("key,value").execute()
        return {row["key"]: row.get("value") for row in response.data or []}
    except Exception as exc:
        _notify_error(f"Supabase settings could not be loaded; using local JSON: {exc}")
        p = _path(SETTINGS_FILENAME)
        if not os.path.exists(p):
            return {}
        try:
            with open(p, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}


def save_settings(settings):
    try:
        client = get_supabase_client(use_service_role=True)
        rows = [{"key": str(key), "value": value} for key, value in settings.items()]
        if rows:
            client.table(SETTINGS_TABLE).upsert(rows, on_conflict="key").execute()
        return True
    except Exception as exc:
        _notify_error(f"Supabase settings could not be saved; using local JSON: {exc}")
        p = _path(SETTINGS_FILENAME)
        with open(p, "w", encoding="utf-8") as f:
            json.dump(settings, f, ensure_ascii=False, indent=2)
        return False


def get_before_land_tips():
    settings = load_settings()
    tips = settings.get("before_land", [])
    if isinstance(tips, str):
        return [tips]
    if not isinstance(tips, list):
        return []
    return tips


def update_before_land_tips(tips):
    settings = load_settings()
    settings["before_land"] = tips
    return save_settings(settings)
