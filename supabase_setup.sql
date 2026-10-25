-- ODMAP — Supabase setup
-- Run this once in your Supabase project: Dashboard > SQL Editor > New query > paste > Run.
-- It creates a table for each user's saved drug list, locked down so users can
-- only read/write their own row (Row Level Security).

create table if not exists public.saved_lists (
  user_id    uuid primary key references auth.users (id) on delete cascade,
  drugs      jsonb not null default '[]'::jsonb,
  updated_at timestamptz not null default now()
);

-- Enable Row Level Security so one user can never see another user's list.
alter table public.saved_lists enable row level security;

-- Each policy restricts rows to the currently authenticated user.
create policy "read own list"
  on public.saved_lists for select
  using (auth.uid() = user_id);

create policy "insert own list"
  on public.saved_lists for insert
  with check (auth.uid() = user_id);

create policy "update own list"
  on public.saved_lists for update
  using (auth.uid() = user_id)
  with check (auth.uid() = user_id);
