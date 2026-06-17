import mimetypes
import os
from pathlib import Path

import pandas as pd

from supabase import create_client


BASE_DIR = Path(__file__).resolve().parents[1]
APPS_CSV = BASE_DIR / "data" / "apps.csv"
BUCKET = os.environ.get("SUPABASE_BUCKET", "internal-assets")
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


def client():
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_SERVICE_ROLE_KEY")
    if not url or not key:
        raise RuntimeError("Set SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY before running this script.")
    return create_client(url, key)


def is_remote_or_data_url(value):
    value = str(value or "").strip().lower()
    return value.startswith(("http://", "https://", "data:"))


def upload_local_asset(supabase, value, folder):
    value = str(value or "").strip()
    if not value or is_remote_or_data_url(value):
        return value

    local_path = BASE_DIR / value.replace("/", os.sep)
    if not local_path.exists() or not local_path.is_file():
        return value

    storage_path = f"{folder}/{local_path.name}"
    content_type = mimetypes.guess_type(local_path.name)[0] or "application/octet-stream"
    with open(local_path, "rb") as file:
        supabase.storage.from_(BUCKET).upload(
            path=storage_path,
            file=file.read(),
            file_options={"content-type": content_type, "upsert": "true"},
        )
    return supabase.storage.from_(BUCKET).get_public_url(storage_path)


def normalize_row(row, supabase):
    data = {}
    for col in APP_COLUMNS:
        data[col] = row.get(col, "" if col not in ("id", "rating") else 0)
    source_download_url = row.get("download_url", "")

    data["id"] = int(data["id"])
    data["rating"] = float(data.get("rating") or 0)
    for col in APP_COLUMNS:
        if col not in ("id", "rating"):
            data[col] = "" if pd.isna(data[col]) else str(data[col])

    source_download_url = "" if pd.isna(source_download_url) else str(source_download_url)
    if source_download_url and not data["app_store_url"] and not data["play_store_url"]:
        if "apps.apple.com" in source_download_url:
            data["app_store_url"] = source_download_url
        elif "play.google.com" in source_download_url:
            data["play_store_url"] = source_download_url

    data["image_url"] = upload_local_asset(supabase, data["image_url"], "app-images")
    in_app_images = []
    for item in data["in_app_images"].split("|"):
        item = item.strip()
        if item:
            in_app_images.append(upload_local_asset(supabase, item, "in-app-images"))
    data["in_app_images"] = "|".join(in_app_images)

    guide_images = []
    for item in data["guide_images"].split("|"):
        item = item.strip()
        if item:
            guide_images.append(upload_local_asset(supabase, item, "guide-images"))
    data["guide_images"] = "|".join(guide_images)
    return data


def main():
    if not APPS_CSV.exists():
        raise RuntimeError(f"Missing CSV file: {APPS_CSV}")

    supabase = client()
    df = pd.read_csv(APPS_CSV)
    for col in APP_COLUMNS:
        if col not in df.columns:
            df[col] = "" if col not in ("id", "rating") else 0

    rows = [normalize_row(row, supabase) for row in df.to_dict("records")]
    if rows:
        supabase.table("apps").upsert(rows, on_conflict="id").execute()
    print(f"Upserted {len(rows)} app rows to Supabase.")


if __name__ == "__main__":
    main()
