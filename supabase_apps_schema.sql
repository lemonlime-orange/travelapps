create table if not exists public.apps (
  id integer primary key,
  name text not null,
  category text not null default '',
  icon text not null default '',
  description text not null default '',
  platform text not null default '',
  rating numeric not null default 0,
  app_store_url text not null default '',
  play_store_url text not null default '',
  features text not null default '',
  tips text not null default '',
  image_url text not null default '',
  guide_images text not null default '',
  guide_image_captions text not null default '',
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

alter table public.apps
  add column if not exists app_store_url text not null default '',
  add column if not exists play_store_url text not null default '',
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
