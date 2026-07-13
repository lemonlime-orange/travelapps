-- Run this once in the Supabase SQL Editor AFTER apps 1-39 have been upserted.
-- No temporary/helper tables are used, so this also works with pooled SQL sessions.

begin;

-- Remove associations belonging to apps that disappeared completely.
delete from public.user_favorites where app_id in (4, 10, 11, 12, 14, 16);
delete from public.user_downloads where app_id in (4, 10, 11, 12, 14, 16);
delete from public.app_reviews where app_id in (4, 10, 11, 12, 14, 16);
delete from public.essential_apps where app_id in (4, 10, 11, 12, 14, 16);

-- Move one favorite ID. The order prevents overlapping moves such as 3 -> 5 -> 20.
do $$
declare
  old_ids integer[] := array[5, 7, 9, 13, 15, 3, 8];
  new_ids integer[] := array[20, 26, 28, 11, 16, 5, 9];
  i integer;
begin
  for i in 1..array_length(old_ids, 1) loop
    insert into public.user_favorites (user_id, app_id, added_at)
    select user_id, new_ids[i], added_at
    from public.user_favorites
    where app_id = old_ids[i]
    on conflict (user_id, app_id) do update
    set added_at = least(public.user_favorites.added_at, excluded.added_at);

    delete from public.user_favorites where app_id = old_ids[i];
  end loop;
end $$;

do $$
declare
  old_ids integer[] := array[5, 7, 9, 13, 15, 3, 8];
  new_ids integer[] := array[20, 26, 28, 11, 16, 5, 9];
  i integer;
begin
  for i in 1..array_length(old_ids, 1) loop
    insert into public.user_downloads (user_id, app_id, downloaded_at)
    select user_id, new_ids[i], downloaded_at
    from public.user_downloads
    where app_id = old_ids[i]
    on conflict (user_id, app_id) do update
    set downloaded_at = least(public.user_downloads.downloaded_at, excluded.downloaded_at);

    delete from public.user_downloads where app_id = old_ids[i];
  end loop;
end $$;

do $$
declare
  old_ids integer[] := array[5, 7, 9, 13, 15, 3, 8];
  new_ids integer[] := array[20, 26, 28, 11, 16, 5, 9];
  i integer;
begin
  for i in 1..array_length(old_ids, 1) loop
    insert into public.app_reviews (
      user_id, username, app_id, rating, review,
      used_after_download, created_at, updated_at
    )
    select
      user_id, username, new_ids[i], rating, review,
      used_after_download, created_at, updated_at
    from public.app_reviews
    where app_id = old_ids[i]
    on conflict (user_id, app_id) do update
    set username = excluded.username,
        rating = excluded.rating,
        review = excluded.review,
        used_after_download = excluded.used_after_download,
        created_at = least(public.app_reviews.created_at, excluded.created_at),
        updated_at = greatest(public.app_reviews.updated_at, excluded.updated_at);

    delete from public.app_reviews where app_id = old_ids[i];
  end loop;
end $$;

do $$
declare
  old_ids integer[] := array[5, 7, 9, 13, 15, 3, 8];
  new_ids integer[] := array[20, 26, 28, 11, 16, 5, 9];
  i integer;
begin
  for i in 1..array_length(old_ids, 1) loop
    insert into public.essential_apps (app_id, created_at)
    select new_ids[i], created_at
    from public.essential_apps
    where app_id = old_ids[i]
    on conflict (app_id) do nothing;

    delete from public.essential_apps where app_id = old_ids[i];
  end loop;
end $$;

-- Normalize situation IDs to pipe-separated values, retain moved apps, and
-- discard removed or malformed values.
update public.situations s
set app_ids = coalesce((
  select string_agg(mapped_id::text, '|' order by first_position)
  from (
    select mapped_id, min(position) as first_position
    from (
      select
        case parsed_id
          when 3 then 5
          when 5 then 20
          when 7 then 26
          when 8 then 9
          when 9 then 28
          when 13 then 11
          when 15 then 16
          else parsed_id
        end as mapped_id,
        position
      from (
        select
          case
            when trim(raw.value) ~ '^\d+$' then trim(raw.value)::integer
            else null
          end as parsed_id,
          raw.position
        from regexp_split_to_table(s.app_ids, '\s*[|,]\s*') with ordinality
          as raw(value, position)
      ) parsed
      where parsed_id is not null
        and parsed_id not in (4, 10, 11, 12, 14, 16)
    ) mapped
    group by mapped_id
  ) deduplicated
), '');

commit;
