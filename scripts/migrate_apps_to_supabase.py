import argparse
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
    "developer",
    "description",
    "platform",
    "rating",
    "downloads",
    "features",
    "tips",
    "app icon",
    "image_url",
    "guide_images",
    "guide_image_captions",
    "app_store_url",
    "play_store_url",
    "in_app_images",
    "in_app_image_captions",
]

REQUIRED_COLUMNS = {
    "id",
    "name",
    "category",
    "description",
    "platform",
    "rating",
    "features",
    "tips",
}


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
    if pd.isna(data["app icon"]) or not str(data["app icon"]).strip():
        data["app icon"] = row.get("icon", "")
    if pd.isna(data["in_app_images"]) or not str(data["in_app_images"]).strip():
        data["in_app_images"] = row.get("in_app_imges", "")
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


def parse_args():
    parser = argparse.ArgumentParser(description="Upsert app data into Supabase.")
    parser.add_argument(
        "csv_path",
        nargs="?",
        type=Path,
        default=APPS_CSV,
        help="CSV to migrate (default: data/apps.csv)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Validate and normalize the CSV without writing to Supabase.",
    )
    return parser.parse_args()


def validate_dataframe(df):
    missing_headers = sorted(REQUIRED_COLUMNS - set(df.columns))
    if missing_headers:
        raise RuntimeError(f"Missing required columns: {', '.join(missing_headers)}")

    duplicate_ids = df.loc[df["id"].duplicated(keep=False), "id"].tolist()
    if duplicate_ids:
        raise RuntimeError(f"Duplicate app IDs: {sorted(set(duplicate_ids))}")

    ids = pd.to_numeric(df["id"], errors="coerce")
    ratings = pd.to_numeric(df["rating"], errors="coerce")
    if ids.isna().any() or (ids % 1 != 0).any():
        raise RuntimeError("Every app ID must be an integer.")
    if ratings.isna().any() or (~ratings.between(0, 5)).any():
        raise RuntimeError("Every rating must be a number between 0 and 5.")

    for col in REQUIRED_COLUMNS - {"id", "rating"}:
        if df[col].isna().any() or (df[col].astype(str).str.strip() == "").any():
            bad_ids = df.loc[
                df[col].isna() | (df[col].astype(str).str.strip() == ""), "id"
            ].tolist()
            raise RuntimeError(f"Column {col!r} is empty for app IDs: {bad_ids}")


def main():
    args = parse_args()
    csv_path = args.csv_path.resolve()
    if not csv_path.exists():
        raise RuntimeError(f"Missing CSV file: {csv_path}")

    df = pd.read_csv(csv_path)
    validate_dataframe(df)
    for col in APP_COLUMNS:
        if col not in df.columns:
            df[col] = "" if col not in ("id", "rating") else 0

    if args.dry_run:
        print(f"Validated {len(df)} app rows from {csv_path}.")
        return

    supabase = client()
    rows = [normalize_row(row, supabase) for row in df.to_dict("records")]
    if rows:
        supabase.table("apps").upsert(rows, on_conflict="id").execute()
    print(f"Upserted {len(rows)} app rows to Supabase.")


if __name__ == "__main__":
    main()
