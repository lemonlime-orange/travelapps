import os

import pandas as pd
from supabase import create_client


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")


def secret(name):
    value = os.environ.get(name)
    if not value:
        raise RuntimeError(f"Missing environment variable: {name}")
    return value


def client():
    return create_client(secret("SUPABASE_URL"), secret("SUPABASE_SERVICE_ROLE_KEY"))


def read_csv(filename, columns):
    path = os.path.join(DATA_DIR, filename)
    if not os.path.exists(path):
        return pd.DataFrame(columns=columns)
    df = pd.read_csv(path, dtype=str).fillna("")
    for column in columns:
        if column not in df.columns:
            df[column] = ""
    return df[columns]


def migrate_users(supabase):
    users = read_csv(
        "users.csv",
        ["user_id", "username", "password_hash", "salt", "email", "created_at"],
    )
    users = users[users["username"].astype(str).str.strip() != ""]
    rows = []
    for row in users.to_dict("records"):
        payload = {
            "username": row["username"],
            "password_hash": row["password_hash"],
            "salt": row["salt"],
            "email": row["email"],
        }
        if row["created_at"]:
            payload["created_at"] = row["created_at"]
        rows.append(payload)
    if rows:
        supabase.table("app_users").upsert(rows, on_conflict="username").execute()

    usernames = [row["username"] for row in users.to_dict("records")]
    response = supabase.table("app_users").select("user_id,username").in_("username", usernames).execute()
    username_to_new_id = {row["username"]: row["user_id"] for row in response.data or []}
    old_to_new_id = {}
    for row in users.to_dict("records"):
        new_id = username_to_new_id.get(row["username"])
        if new_id is not None:
            old_to_new_id[str(row["user_id"])] = int(new_id)
    print(f"Migrated users: {len(rows)}")
    return old_to_new_id


def migrate_user_apps(supabase, filename, table_name, timestamp_column, user_id_map):
    df = read_csv(filename, ["user_id", "app_id", timestamp_column])
    df = df[(df["user_id"].astype(str).str.strip() != "") & (df["app_id"].astype(str).str.strip() != "")]
    rows = []
    for row in df.to_dict("records"):
        mapped_user_id = user_id_map.get(str(row["user_id"]))
        if mapped_user_id is None:
            continue
        payload = {
            "user_id": mapped_user_id,
            "app_id": int(row["app_id"]),
        }
        if row[timestamp_column]:
            payload[timestamp_column] = row[timestamp_column]
        rows.append(payload)
    if rows:
        supabase.table(table_name).upsert(rows, on_conflict="user_id,app_id").execute()
    print(f"Migrated {table_name}: {len(rows)}")


def migrate_app_reviews(supabase, user_id_map):
    df = read_csv(
        "app_reviews.csv",
        [
            "user_id",
            "username",
            "app_id",
            "rating",
            "review",
            "used_after_download",
            "created_at",
            "updated_at",
        ],
    )
    df = df[(df["user_id"].astype(str).str.strip() != "") & (df["app_id"].astype(str).str.strip() != "")]
    rows = []
    for row in df.to_dict("records"):
        mapped_user_id = user_id_map.get(str(row["user_id"]))
        if mapped_user_id is None:
            continue
        payload = {
            "user_id": mapped_user_id,
            "username": row["username"] or "Traveler",
            "app_id": int(row["app_id"]),
            "rating": float(row["rating"] or 0),
            "review": row["review"],
            "used_after_download": str(row["used_after_download"]).lower() in ("true", "1", "yes", "y"),
        }
        if row["created_at"]:
            payload["created_at"] = row["created_at"]
        if row["updated_at"]:
            payload["updated_at"] = row["updated_at"]
        rows.append(payload)
    if rows:
        supabase.table("app_reviews").upsert(rows, on_conflict="user_id,app_id").execute()
    print(f"Migrated app_reviews: {len(rows)}")


def main():
    supabase = client()
    user_id_map = migrate_users(supabase)
    migrate_user_apps(supabase, "user_favorites.csv", "user_favorites", "added_at", user_id_map)
    migrate_user_apps(supabase, "user_downloads.csv", "user_downloads", "downloaded_at", user_id_map)
    migrate_app_reviews(supabase, user_id_map)


if __name__ == "__main__":
    main()
