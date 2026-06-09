import json
import os
from pathlib import Path

import pandas as pd
from supabase import create_client


BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data"
SITUATIONS_CSV = DATA_DIR / "situations.csv"
SETTINGS_JSON = DATA_DIR / "settings.json"

SITUATION_COLUMNS = [
    "id",
    "situation",
    "emoji",
    "description",
    "category",
    "app_ids",
]


def client():
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_SERVICE_ROLE_KEY")
    if not url or not key:
        raise RuntimeError("Set SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY before running this script.")
    return create_client(url, key)


def situation_payload(row):
    payload = {}
    for col in SITUATION_COLUMNS:
        value = row.get(col, 0 if col == "id" else "")
        if pd.isna(value):
            value = 0 if col == "id" else ""
        payload[col] = int(value) if col == "id" else str(value)
    return payload


def migrate_situations(supabase):
    if not SITUATIONS_CSV.exists():
        print(f"Skipped situations: missing {SITUATIONS_CSV}")
        return

    df = pd.read_csv(SITUATIONS_CSV)
    for col in SITUATION_COLUMNS:
        if col not in df.columns:
            df[col] = 0 if col == "id" else ""

    rows = [situation_payload(row) for row in df.to_dict("records")]
    if rows:
        supabase.table("situations").upsert(rows, on_conflict="id").execute()
    print(f"Upserted {len(rows)} situation rows to Supabase.")


def migrate_settings(supabase):
    if not SETTINGS_JSON.exists():
        print(f"Skipped settings: missing {SETTINGS_JSON}")
        return

    with open(SETTINGS_JSON, "r", encoding="utf-8") as file:
        settings = json.load(file)

    rows = [{"key": str(key), "value": value} for key, value in settings.items()]
    if rows:
        supabase.table("app_settings").upsert(rows, on_conflict="key").execute()
    print(f"Upserted {len(rows)} setting rows to Supabase.")


def main():
    supabase = client()
    migrate_situations(supabase)
    migrate_settings(supabase)


if __name__ == "__main__":
    main()
