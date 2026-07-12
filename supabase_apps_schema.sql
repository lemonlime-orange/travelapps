create table if not exists public.apps (
  id integer primary key,
  name text not null,
  category text not null default '',
  developer text not null default '',
  description text not null default '',
  platform text not null default '',
  rating numeric not null default 0,
  downloads text not null default '',
  features text not null default '',
  tips text not null default '',
  "app icon" text not null default '',
  image_url text not null default '',
  guide_images text not null default '',
  guide_image_captions text not null default '',
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  app_store_url text not null default '',
  play_store_url text not null default '',
  in_app_images text not null default '',
  in_app_image_captions text not null default ''
);

do $$
begin
  if exists (
    select 1
    from information_schema.columns
    where table_schema = 'public'
      and table_name = 'apps'
      and column_name = 'icon'
  ) and exists (
    select 1
    from information_schema.columns
    where table_schema = 'public'
      and table_name = 'apps'
      and column_name = 'app icon'
  ) then
    update public.apps
    set "app icon" = icon
    where coalesce("app icon", '') = ''
      and coalesce(icon, '') <> '';
    alter table public.apps drop column icon;
  elsif exists (
    select 1
    from information_schema.columns
    where table_schema = 'public'
      and table_name = 'apps'
      and column_name = 'icon'
  ) and not exists (
    select 1
    from information_schema.columns
    where table_schema = 'public'
      and table_name = 'apps'
      and column_name = 'app icon'
  ) then
    alter table public.apps rename column icon to "app icon";
  end if;

  if exists (
    select 1
    from information_schema.columns
    where table_schema = 'public'
      and table_name = 'apps'
      and column_name = 'in_app_imges'
  ) and exists (
    select 1
    from information_schema.columns
    where table_schema = 'public'
      and table_name = 'apps'
      and column_name = 'in_app_images'
  ) then
    update public.apps
    set in_app_images = in_app_imges
    where coalesce(in_app_images, '') = ''
      and coalesce(in_app_imges, '') <> '';
    alter table public.apps drop column in_app_imges;
  elsif exists (
    select 1
    from information_schema.columns
    where table_schema = 'public'
      and table_name = 'apps'
      and column_name = 'in_app_imges'
  ) and not exists (
    select 1
    from information_schema.columns
    where table_schema = 'public'
      and table_name = 'apps'
      and column_name = 'in_app_images'
  ) then
    alter table public.apps rename column in_app_imges to in_app_images;
  end if;
end $$;

alter table public.apps
  add column if not exists developer text not null default '',
  add column if not exists downloads text not null default '',
  add column if not exists "app icon" text not null default '',
  add column if not exists app_store_url text not null default '',
  add column if not exists play_store_url text not null default '',
  add column if not exists in_app_images text not null default '',
  add column if not exists in_app_image_captions text not null default '',
  add column if not exists guide_images text not null default '',
  add column if not exists guide_image_captions text not null default '',
  drop column if exists download_url;

create or replace function public.set_updated_at()
returns trigger
language plpgsql
as $$
begin
  new.updated_at = now();
  return new;
end;
$$;

drop trigger if exists set_apps_updated_at on public.apps;

create trigger set_apps_updated_at
before update on public.apps
for each row
execute function public.set_updated_at();

alter table public.apps enable row level security;

drop policy if exists "Allow public app reads" on public.apps;

create policy "Allow public app reads"
on public.apps
for select
using (true);

-- Essential Apps membership is kept separately from general app categories.
create table if not exists public.essential_apps (
  app_id integer primary key references public.apps(id) on delete cascade,
  created_at timestamptz not null default now()
);

-- Preserve existing Essential Apps selections when this schema is first applied.
insert into public.essential_apps (app_id)
select id
from public.apps
where 'Essential Apps' = any (string_to_array(category, '|'))
on conflict (app_id) do nothing;

-- Essential Apps is no longer a general category.
update public.apps
set category = array_to_string(
  array_remove(string_to_array(category, '|'), 'Essential Apps'),
  '|'
)
where 'Essential Apps' = any (string_to_array(category, '|'));

alter table public.essential_apps enable row level security;

drop policy if exists "Allow public essential app reads" on public.essential_apps;

create policy "Allow public essential app reads"
on public.essential_apps
for select
using (true);

create table if not exists public.situations (
  id integer primary key,
  situation text not null default '',
  emoji text not null default '',
  description text not null default '',
  category text not null default '',
  app_ids text not null default '',
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

drop trigger if exists set_situations_updated_at on public.situations;

create trigger set_situations_updated_at
before update on public.situations
for each row
execute function public.set_updated_at();

alter table public.situations enable row level security;

drop policy if exists "Allow public situation reads" on public.situations;

create policy "Allow public situation reads"
on public.situations
for select
using (true);

create table if not exists public.app_settings (
  key text primary key,
  value jsonb not null default 'null'::jsonb,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

drop trigger if exists set_app_settings_updated_at on public.app_settings;

create trigger set_app_settings_updated_at
before update on public.app_settings
for each row
execute function public.set_updated_at();

alter table public.app_settings enable row level security;

drop policy if exists "Allow public setting reads" on public.app_settings;

create policy "Allow public setting reads"
on public.app_settings
for select
using (true);

create table if not exists public.app_users (
  user_id bigint generated by default as identity primary key,
  username text not null unique,
  password_hash text not null default '',
  salt text not null default '',
  email text not null default '',
  created_at timestamptz not null default now()
);

insert into public.app_users (user_id, username, password_hash, salt, email)
values (0, 'guest', '', '', '')
on conflict (username) do nothing;

alter table public.app_users enable row level security;

create table if not exists public.user_favorites (
  user_id bigint not null references public.app_users(user_id) on delete cascade,
  app_id integer not null references public.apps(id) on delete cascade,
  added_at timestamptz not null default now(),
  primary key (user_id, app_id)
);

alter table public.user_favorites enable row level security;

create table if not exists public.user_downloads (
  user_id bigint not null references public.app_users(user_id) on delete cascade,
  app_id integer not null references public.apps(id) on delete cascade,
  downloaded_at timestamptz not null default now(),
  primary key (user_id, app_id)
);

alter table public.user_downloads enable row level security;

create table if not exists public.app_reviews (
  user_id bigint not null references public.app_users(user_id) on delete cascade,
  username text not null default '',
  app_id integer not null references public.apps(id) on delete cascade,
  rating numeric not null default 0,
  review text not null default '',
  used_after_download boolean not null default true,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  primary key (user_id, app_id),
  constraint app_reviews_rating_range check (rating >= 0 and rating <= 5)
);

drop trigger if exists set_app_reviews_updated_at on public.app_reviews;

create trigger set_app_reviews_updated_at
before update on public.app_reviews
for each row
execute function public.set_updated_at();

alter table public.app_reviews enable row level security;
