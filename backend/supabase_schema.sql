-- ==============================================================================
-- ClockEE Master Supabase Schema & Row-Level Security (RLS) Policy Definition
-- Autonomous JEE Advanced Cockpit & Cognitive CBT Engine
-- ==============================================================================

-- 1. Enable Required Extensions
create extension if not exists "uuid-ossp";
create extension if not exists "pgcrypto";

-- ==============================================================================
-- 2. TABLE: public.profiles
-- User profile linked directly to Supabase Auth (auth.users)
-- ==============================================================================
create table if not exists public.profiles (
    id uuid primary key references auth.users(id) on delete cascade,
    email text unique not null,
    full_name text not null default 'JEE Aspirant',
    avatar_url text default 'https://api.dicebear.com/7.x/bottts-neutral/svg?seed=Aspirant',
    role text not null default 'JEE 2028 Aspirant',
    theme_preference text not null default 'cyan_indigo',
    aura_mode text not null default 'fluid',
    created_at timestamptz not null default now(),
    last_seen timestamptz not null default now()
);

-- ==============================================================================
-- 3. TABLE: public.student_states
-- Active state snapshot (timer, study mode, active decks, daily goals)
-- ==============================================================================
create table if not exists public.student_states (
    user_id uuid primary key references auth.users(id) on delete cascade,
    current_mode text not null default 'mains',
    timer_state jsonb not null default '{}'::jsonb,
    active_deck text not null default '',
    daily_goals jsonb not null default '{"Physics": 30, "Chemistry": 30, "Maths": 30, "hours": 6.0}'::jsonb,
    stats jsonb not null default '{"hoursToday": 0.0, "streakDays": 1, "questionsSolved": {"Physics": 0, "Chemistry": 0, "Maths": 0}}'::jsonb,
    state_payload jsonb not null default '{}'::jsonb,
    updated_at timestamptz not null default now()
);

-- ==============================================================================
-- 4. TABLE: public.cbt_results
-- Comprehensive CBT Examination results and answer telemetry
-- ==============================================================================
create table if not exists public.cbt_results (
    id uuid primary key default gen_random_uuid(),
    user_id uuid not null references auth.users(id) on delete cascade,
    test_id text not null,
    title text not null default 'CBT Mock Examination',
    mode text not null default 'mains',
    subject text not null default 'Full',
    chapter text default '',
    total_questions int not null default 25,
    score int not null default 0,
    max_score int not null default 100,
    accuracy numeric(5, 2) not null default 0.00,
    time_spent int not null default 0,
    answers_json jsonb not null default '[]'::jsonb,
    analytics_json jsonb not null default '{}'::jsonb,
    completed_at timestamptz not null default now()
);

-- ==============================================================================
-- 5. TABLE: public.study_sessions
-- Question sprint logs, mistake autopsy sequences & study sessions
-- ==============================================================================
create table if not exists public.study_sessions (
    id uuid primary key default gen_random_uuid(),
    user_id uuid not null references auth.users(id) on delete cascade,
    duration_seconds numeric(8, 2) not null default 0.00,
    subject text not null default 'Physics',
    topic text not null default 'General',
    chapter text default '',
    question_num int default 1,
    is_correct boolean default true,
    mistake_tag text default '',
    score_delta int default 4,
    notes text default '',
    timestamp timestamptz not null default now()
);

-- ==============================================================================
-- 6. INDEXES FOR HIGH-THROUGHPUT QUERYING
-- ==============================================================================
create index if not exists idx_profiles_email on public.profiles(email);
create index if not exists idx_student_states_updated on public.student_states(updated_at desc);
create index if not exists idx_cbt_results_user on public.cbt_results(user_id, completed_at desc);
create index if not exists idx_cbt_results_test_id on public.cbt_results(test_id);
create index if not exists idx_study_sessions_user_ts on public.study_sessions(user_id, timestamp desc);
create index if not exists idx_study_sessions_subject on public.study_sessions(user_id, subject);

-- ==============================================================================
-- 7. ROW-LEVEL SECURITY (RLS) POLICIES
-- Strict Isolation: Users may SELECT, INSERT, UPDATE, DELETE only rows where auth.uid() = user_id (or id)
-- ==============================================================================

-- 7.1 Profiles RLS
alter table public.profiles enable row level security;

drop policy if exists "Users can view own profile" on public.profiles;
create policy "Users can view own profile"
    on public.profiles
    for select
    using (auth.uid() = id);

drop policy if exists "Users can update own profile" on public.profiles;
create policy "Users can update own profile"
    on public.profiles
    for update
    using (auth.uid() = id)
    with check (auth.uid() = id);

drop policy if exists "Users can insert own profile" on public.profiles;
create policy "Users can insert own profile"
    on public.profiles
    for insert
    with check (auth.uid() = id);

-- 7.2 Student States RLS
alter table public.student_states enable row level security;

drop policy if exists "Users can view own student state" on public.student_states;
create policy "Users can view own student state"
    on public.student_states
    for select
    using (auth.uid() = user_id);

drop policy if exists "Users can insert own student state" on public.student_states;
create policy "Users can insert own student state"
    on public.student_states
    for insert
    with check (auth.uid() = user_id);

drop policy if exists "Users can update own student state" on public.student_states;
create policy "Users can update own student state"
    on public.student_states
    for update
    using (auth.uid() = user_id)
    with check (auth.uid() = user_id);

drop policy if exists "Users can delete own student state" on public.student_states;
create policy "Users can delete own student state"
    on public.student_states
    for delete
    using (auth.uid() = user_id);

-- 7.3 CBT Results RLS
alter table public.cbt_results enable row level security;

drop policy if exists "Users can view own CBT results" on public.cbt_results;
create policy "Users can view own CBT results"
    on public.cbt_results
    for select
    using (auth.uid() = user_id);

drop policy if exists "Users can insert own CBT results" on public.cbt_results;
create policy "Users can insert own CBT results"
    on public.cbt_results
    for insert
    with check (auth.uid() = user_id);

drop policy if exists "Users can update own CBT results" on public.cbt_results;
create policy "Users can update own CBT results"
    on public.cbt_results
    for update
    using (auth.uid() = user_id)
    with check (auth.uid() = user_id);

drop policy if exists "Users can delete own CBT results" on public.cbt_results;
create policy "Users can delete own CBT results"
    on public.cbt_results
    for delete
    using (auth.uid() = user_id);

-- 7.4 Study Sessions RLS
alter table public.study_sessions enable row level security;

drop policy if exists "Users can view own study sessions" on public.study_sessions;
create policy "Users can view own study sessions"
    on public.study_sessions
    for select
    using (auth.uid() = user_id);

drop policy if exists "Users can insert own study sessions" on public.study_sessions;
create policy "Users can insert own study sessions"
    on public.study_sessions
    for insert
    with check (auth.uid() = user_id);

drop policy if exists "Users can update own study sessions" on public.study_sessions;
create policy "Users can update own study sessions"
    on public.study_sessions
    for update
    using (auth.uid() = user_id)
    with check (auth.uid() = user_id);

drop policy if exists "Users can delete own study sessions" on public.study_sessions;
create policy "Users can delete own study sessions"
    on public.study_sessions
    for delete
    using (auth.uid() = user_id);

-- ==============================================================================
-- 8. AUTOMATIC PROFILE PROVISIONING TRIGGER (on auth.users insertion)
-- ==============================================================================
create or replace function public.handle_new_user()
returns trigger
security definer
set search_path = public
language plpgsql
as $$
begin
    insert into public.profiles (id, email, full_name, avatar_url, role)
    values (
        new.id,
        new.email,
        coalesce(new.raw_user_meta_data->>'full_name', new.raw_user_meta_data->>'name', split_part(new.email, '@', 1)),
        coalesce(new.raw_user_meta_data->>'avatar_url', 'https://api.dicebear.com/7.x/bottts-neutral/svg?seed=' || coalesce(new.raw_user_meta_data->>'name', split_part(new.email, '@', 1))),
        coalesce(new.raw_user_meta_data->>'role', 'JEE 2028 Aspirant')
    )
    on conflict (id) do nothing;

    insert into public.student_states (user_id, current_mode, timer_state, daily_goals, stats)
    values (
        new.id,
        'mains',
        '{}'::jsonb,
        '{"Physics": 30, "Chemistry": 30, "Maths": 30, "hours": 6.0}'::jsonb,
        '{"hoursToday": 0.0, "streakDays": 1, "questionsSolved": {"Physics": 0, "Chemistry": 0, "Maths": 0}}'::jsonb
    )
    on conflict (user_id) do nothing;

    return new;
end;
$$;

-- Trigger firing on every new Supabase Auth user registration (email, Google, GitHub)
drop trigger if exists on_auth_user_created on auth.users;
create trigger on_auth_user_created
    after insert on auth.users
    for each row execute function public.handle_new_user();
