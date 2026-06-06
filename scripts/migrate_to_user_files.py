import csv
import os
import shutil
from datetime import datetime


def ensure_file(path, header):
    if not os.path.exists(path):
        with open(path, 'w', newline='', encoding='utf-8') as f:
            f.write(header + '\n')


def read_rows(path, key_field='app_id'):
    rows = []
    if not os.path.exists(path):
        return rows
    with open(path, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for r in reader:
            if key_field in r and r[key_field].strip():
                rows.append(r[key_field].strip())
    return rows


def append_row(path, fieldnames, row):
    exists = os.path.exists(path) and os.path.getsize(path) > 0
    with open(path, 'a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if os.path.getsize(path) == 0:
            writer.writeheader()
        writer.writerow(row)


def migrate():
    base = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    data_dir = os.path.join(base, 'data')

    old_fav = os.path.join(data_dir, 'favorites.csv')
    old_dl = os.path.join(data_dir, 'downloads.csv')
    users = os.path.join(data_dir, 'users.csv')
    user_fav = os.path.join(data_dir, 'user_favorites.csv')
    user_dl = os.path.join(data_dir, 'user_downloads.csv')

    # Ensure target files exist (headers already present by previous step, but safe)
    ensure_file(users, 'user_id,username,password_hash,salt,email,created_at')
    ensure_file(user_fav, 'user_id,app_id,added_at')
    ensure_file(user_dl, 'user_id,app_id,downloaded_at')

    # Load users to see if any exist
    existing_users = []
    with open(users, newline='', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for r in reader:
            if r.get('user_id'):
                existing_users.append(r)

    if not existing_users:
        # create a guest/global user with id 0
        guest = {
            'user_id': '0',
            'username': 'guest',
            'password_hash': '',
            'salt': '',
            'email': '',
            'created_at': datetime.utcnow().isoformat() + 'Z'
        }
        append_row(users, ['user_id','username','password_hash','salt','email','created_at'], guest)
        user_id = '0'
    else:
        user_id = existing_users[0]['user_id']

    # Backup old files
    backup_dir = os.path.join(data_dir, 'backup')
    os.makedirs(backup_dir, exist_ok=True)
    if os.path.exists(old_fav):
        shutil.copy(old_fav, os.path.join(backup_dir, 'favorites.csv.bak'))
    if os.path.exists(old_dl):
        shutil.copy(old_dl, os.path.join(backup_dir, 'downloads.csv.bak'))

    fav_app_ids = read_rows(old_fav, 'app_id')
    dl_app_ids = read_rows(old_dl, 'app_id')

    count_fav = 0
    count_dl = 0
    now = datetime.utcnow().isoformat() + 'Z'

    for app_id in fav_app_ids:
        append_row(user_fav, ['user_id','app_id','added_at'], {'user_id': user_id, 'app_id': app_id, 'added_at': now})
        count_fav += 1

    for app_id in dl_app_ids:
        append_row(user_dl, ['user_id','app_id','downloaded_at'], {'user_id': user_id, 'app_id': app_id, 'downloaded_at': now})
        count_dl += 1

    print(f'Migration complete. favorites -> {count_fav} rows; downloads -> {count_dl} rows; user_id used: {user_id}')


if __name__ == '__main__':
    migrate()
