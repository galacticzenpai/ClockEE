-- ==============================================================================
-- ClockEE SQLite to Supabase PostgreSQL Migration Dump
-- Generated at: 2026-11-16T10:24:58.532808
-- ==============================================================================
BEGIN;

-- 1. Insert / Upsert Profiles
INSERT INTO public.profiles (id, email, full_name, avatar_url, role, theme_preference, aura_mode, created_at, last_seen)
VALUES ('00000000-0000-4000-a000-000000000001', 'supabase_aspirant@clockee.app', 'supabase_aspirant', 'https://api.dicebear.com/7.x/bottts-neutral/svg?seed=supabase_aspirant', 'authenticated', 'cyan_indigo', 'fluid', '2026-11-16 04:53:16', '2026-11-16 04:53:16')
ON CONFLICT (id) DO UPDATE SET
    full_name = EXCLUDED.full_name,
    avatar_url = EXCLUDED.avatar_url,
    role = EXCLUDED.role,
    theme_preference = EXCLUDED.theme_preference,
    aura_mode = EXCLUDED.aura_mode,
    last_seen = EXCLUDED.last_seen;
INSERT INTO public.profiles (id, email, full_name, avatar_url, role, theme_preference, aura_mode, created_at, last_seen)
VALUES ('96ede7d1-0ad8-5be9-a570-7d918d5d626e', 'alpha@clockee.app', 'Student Alpha', 'https://api.dicebear.com/7.x/bottts-neutral/svg?seed=AlphaCommander', 'JEE 2028 Aspirant', 'space_violet', 'pulse', '2026-11-16 04:54:50', '2026-11-16 04:54:55')
ON CONFLICT (id) DO UPDATE SET
    full_name = EXCLUDED.full_name,
    avatar_url = EXCLUDED.avatar_url,
    role = EXCLUDED.role,
    theme_preference = EXCLUDED.theme_preference,
    aura_mode = EXCLUDED.aura_mode,
    last_seen = EXCLUDED.last_seen;
INSERT INTO public.profiles (id, email, full_name, avatar_url, role, theme_preference, aura_mode, created_at, last_seen)
VALUES ('d909fe12-3fb3-5334-8f5c-a5433f59d8bf', 'beta@clockee.app', 'Student Beta', 'https://api.dicebear.com/7.x/bottts-neutral/svg?seed=BetaAspirant', 'JEE 2028 Aspirant', 'cyan_indigo', 'fluid', '2026-11-16 04:54:50', '2026-11-16 04:54:50')
ON CONFLICT (id) DO UPDATE SET
    full_name = EXCLUDED.full_name,
    avatar_url = EXCLUDED.avatar_url,
    role = EXCLUDED.role,
    theme_preference = EXCLUDED.theme_preference,
    aura_mode = EXCLUDED.aura_mode,
    last_seen = EXCLUDED.last_seen;
INSERT INTO public.profiles (id, email, full_name, avatar_url, role, theme_preference, aura_mode, created_at, last_seen)
VALUES ('605f8b62-203a-5b79-9b7d-d610d22755e9', 'admin@clockee.app', 'Master Admin & Mentor', 'https://api.dicebear.com/7.x/bottts-neutral/svg?seed=ClockEECommander', 'Mentor / Faculty', 'cyan_indigo', 'fluid', '2026-11-16 04:54:50', '2026-11-16 04:54:50')
ON CONFLICT (id) DO UPDATE SET
    full_name = EXCLUDED.full_name,
    avatar_url = EXCLUDED.avatar_url,
    role = EXCLUDED.role,
    theme_preference = EXCLUDED.theme_preference,
    aura_mode = EXCLUDED.aura_mode,
    last_seen = EXCLUDED.last_seen;

-- 2. Insert / Upsert Student States
INSERT INTO public.student_states (user_id, current_mode, timer_state, active_deck, daily_goals, stats, state_payload, updated_at)
VALUES ('00000000-0000-4000-a000-000000000001', 'mains', '{}'::jsonb, '', '{"Physics": 30, "Chemistry": 30, "Maths": 30, "hours": 6.0}'::jsonb, '{"hoursToday": 0.0, "streakDays": 1, "questionsSolved": {"Physics": 0, "Chemistry": 0, "Maths": 0}}'::jsonb, '{"profile": {"name": "supabase_aspirant", "subtitle": "authenticated • Cloud Account", "pfp": "https://api.dicebear.com/7.x/bottts-neutral/svg?seed=supabase_aspirant"}, "examMode": "mains", "dailyGoals": {"Physics": 30, "Chemistry": 30, "Maths": 30, "hours": 6.0}, "theme_preference": "cyan_indigo", "aura_mode": "fluid", "stats": {"hoursToday": 0.0, "streakDays": 1, "questionsSolved": {"Physics": 0, "Chemistry": 0, "Maths": 0}}}'::jsonb, '2026-11-16 04:53:16')
ON CONFLICT (user_id) DO UPDATE SET
    current_mode = EXCLUDED.current_mode,
    timer_state = EXCLUDED.timer_state,
    active_deck = EXCLUDED.active_deck,
    daily_goals = EXCLUDED.daily_goals,
    stats = EXCLUDED.stats,
    state_payload = EXCLUDED.state_payload,
    updated_at = EXCLUDED.updated_at;
INSERT INTO public.student_states (user_id, current_mode, timer_state, active_deck, daily_goals, stats, state_payload, updated_at)
VALUES ('96ede7d1-0ad8-5be9-a570-7d918d5d626e', 'advanced', '{"elapsed_seconds": 3600, "mode": "sprint", "is_paused": false}'::jsonb, 'Rotational Mechanics Mastery', '{"Physics": 35, "Chemistry": 35, "Maths": 35, "hours": 7.5}'::jsonb, '{"hoursToday": 5.8, "streakDays": 14, "questionsSolved": {"Physics": 64, "Chemistry": 58, "Maths": 63}, "todayTarget": 105}'::jsonb, '{"profile": {"name": "Student Alpha", "subtitle": "JEE 2028 Advanced • IIT Bombay Target (AIR < 50)", "pfp": "https://api.dicebear.com/7.x/bottts-neutral/svg?seed=AlphaCommander", "accent": "#00f2fe"}, "examMode": "advanced", "dailyGoals": {"Physics": 35, "Chemistry": 35, "Maths": 35, "hours": 7.5}, "jeeDate": "2028-05-17", "nextMilestone": {"date": "2026-11-20", "title": "Phase Major Test #01 (Rotational Dynamics & Thermodynamics)"}, "settings": {"auraTheme": "space_violet", "auraSpeed": "pulse"}, "apiKeys": {"ticktick": "", "gemini": "", "cloudUrl": "http://127.0.0.1:8000"}, "stats": {"hoursToday": 5.8, "streakDays": 14, "questionsSolved": {"Physics": 64, "Chemistry": 58, "Maths": 63}, "todayTarget": 105}, "tasks": [{"id": "task_a1", "title": "Solve Irodov 1.15 to 1.30 (Rigid Body Rotational Dynamics)", "subject": "Physics", "priority": "high", "completed": false}, {"id": "task_a2", "title": "Review GOC Electrophilic Addition Reaction Mechanisms", "subject": "Chemistry", "priority": "medium", "completed": false}, {"id": "task_a3", "title": "Master Definite Integrals with Leibniz Rule PYQs (2020-2025)", "subject": "Maths", "priority": "high", "completed": false}, {"id": "task_a4", "title": "Complete Chemistry CBT Latency Speed Drill", "subject": "Chemistry", "priority": "low", "completed": true}], "questionLogs": [{"id": "log_a1", "subject": "Physics", "chapter": "Rotational Motion", "qNum": 1, "duration": 42.4, "correct": true, "notes": "Moment of inertia of composite cone", "timestamp": "2026-11-15T18:10:00Z"}, {"id": "log_a2", "subject": "Physics", "chapter": "Rotational Motion", "qNum": 2, "duration": 88.1, "correct": false, "mistake": "calculation", "notes": "Missed parallel axis theorem offset d^2 term", "timestamp": "2026-11-15T18:12:00Z"}, {"id": "log_a3", "subject": "Chemistry", "chapter": "Thermodynamics", "qNum": 1, "duration": 52.0, "correct": true, "notes": "Adiabatic expansion reversible vs irreversible work done", "timestamp": "2026-11-15T19:00:00Z"}, {"id": "log_a4", "subject": "Maths", "chapter": "Definite Integration", "qNum": 1, "duration": 110.5, "correct": true, "notes": "King''s property f(a+b-x) symmetry", "timestamp": "2026-11-15T20:15:00Z"}], "mockTests": [{"testId": "cbt_mock_001", "title": "JEE Advanced 2025 Paper-1 Full Mock", "score": 248, "maxScore": 360, "accuracy": 82.5, "date": "2026-11-14T14:30:00Z", "breakdown": {"Physics": 84, "Chemistry": 88, "Maths": 76}}], "customization_token": "token_halo_violet_99", "glass_blur": 32, "theme_preference": "space_violet", "aura_mode": "pulse", "timer_state": {"elapsed_seconds": 3600, "mode": "sprint", "is_paused": false}, "activeDeck": "Rotational Mechanics Mastery"}'::jsonb, '2026-11-16 04:54:58')
ON CONFLICT (user_id) DO UPDATE SET
    current_mode = EXCLUDED.current_mode,
    timer_state = EXCLUDED.timer_state,
    active_deck = EXCLUDED.active_deck,
    daily_goals = EXCLUDED.daily_goals,
    stats = EXCLUDED.stats,
    state_payload = EXCLUDED.state_payload,
    updated_at = EXCLUDED.updated_at;
INSERT INTO public.student_states (user_id, current_mode, timer_state, active_deck, daily_goals, stats, state_payload, updated_at)
VALUES ('d909fe12-3fb3-5334-8f5c-a5433f59d8bf', 'mains', '{}'::jsonb, '', '{"Physics": 30, "Chemistry": 30, "Maths": 30, "hours": 6.0}'::jsonb, '{"hoursToday": 3.2, "streakDays": 4, "questionsSolved": {"Physics": 18, "Chemistry": 22, "Maths": 20}, "todayTarget": 90}'::jsonb, '{"profile": {"name": "Student Beta", "subtitle": "JEE 2028 Aspirant • Strict Cloud Isolation", "pfp": "https://api.dicebear.com/7.x/bottts-neutral/svg?seed=BetaAspirant", "accent": "#a855f7"}, "examMode": "mains", "dailyGoals": {"Physics": 30, "Chemistry": 30, "Maths": 30, "hours": 6.0}, "jeeDate": "2028-05-17", "nextMilestone": {"date": "2026-11-22", "title": "Coaching Phase Unit Test #02"}, "settings": {"auraTheme": "cyan_indigo", "auraSpeed": "fluid"}, "apiKeys": {"ticktick": "", "gemini": "", "cloudUrl": "http://127.0.0.1:8000"}, "stats": {"hoursToday": 3.2, "streakDays": 4, "questionsSolved": {"Physics": 18, "Chemistry": 22, "Maths": 20}, "todayTarget": 90}, "tasks": [{"id": "task_b1", "title": "Kinematics Relative Velocity Projectile Problems", "subject": "Physics", "priority": "high", "completed": false}, {"id": "task_b2", "title": "Chemical Bonding Molecular Orbital Theory Diagrams", "subject": "Chemistry", "priority": "medium", "completed": false}], "questionLogs": [{"id": "log_b1", "subject": "Physics", "chapter": "Kinematics", "qNum": 1, "duration": 55.0, "correct": true, "notes": "Rain man relative vector approach", "timestamp": "2026-11-15T15:00:00Z"}], "mockTests": [], "theme_preference": "cyan_indigo", "aura_mode": "fluid"}'::jsonb, '2026-11-16 04:54:57')
ON CONFLICT (user_id) DO UPDATE SET
    current_mode = EXCLUDED.current_mode,
    timer_state = EXCLUDED.timer_state,
    active_deck = EXCLUDED.active_deck,
    daily_goals = EXCLUDED.daily_goals,
    stats = EXCLUDED.stats,
    state_payload = EXCLUDED.state_payload,
    updated_at = EXCLUDED.updated_at;
INSERT INTO public.student_states (user_id, current_mode, timer_state, active_deck, daily_goals, stats, state_payload, updated_at)
VALUES ('605f8b62-203a-5b79-9b7d-d610d22755e9', 'mains', '{}'::jsonb, '', '{"Physics": 30, "Chemistry": 30, "Maths": 30, "hours": 6.0}'::jsonb, '{"hoursToday": 0.0, "streakDays": 1, "questionsSolved": {"Physics": 0, "Chemistry": 0, "Maths": 0}}'::jsonb, '{"profile": {"name": "Master Admin & Mentor", "subtitle": "Director of Academic Roster & System Architecture", "pfp": "https://api.dicebear.com/7.x/bottts-neutral/svg?seed=ClockEECommander", "accent": "#6366f1"}, "role": "Mentor / Faculty", "isAdmin": true, "settings": {"dynamicAura": true, "auraTheme": "cyan_indigo", "auraSpeed": "fluid"}}'::jsonb, '2026-11-16 04:54:50')
ON CONFLICT (user_id) DO UPDATE SET
    current_mode = EXCLUDED.current_mode,
    timer_state = EXCLUDED.timer_state,
    active_deck = EXCLUDED.active_deck,
    daily_goals = EXCLUDED.daily_goals,
    stats = EXCLUDED.stats,
    state_payload = EXCLUDED.state_payload,
    updated_at = EXCLUDED.updated_at;

-- 3. Insert Study Sessions
INSERT INTO public.study_sessions (id, user_id, duration_seconds, subject, topic, chapter, question_num, is_correct, mistake_tag, score_delta, notes, timestamp)
VALUES ('14522298-f627-5b60-845d-a1efc4602598', '96ede7d1-0ad8-5be9-a570-7d918d5d626e', 42.4, 'Physics', 'Rotational Motion', 'Rotational Motion', 1, TRUE, '', 4, 'Moment of inertia of composite cone', '2026-11-16 04:54:50')
ON CONFLICT (id) DO NOTHING;
INSERT INTO public.study_sessions (id, user_id, duration_seconds, subject, topic, chapter, question_num, is_correct, mistake_tag, score_delta, notes, timestamp)
VALUES ('c06134d5-4523-59d3-b49b-43c17ce8f7d6', '96ede7d1-0ad8-5be9-a570-7d918d5d626e', 88.1, 'Physics', 'Rotational Motion', 'Rotational Motion', 2, FALSE, 'calculation', 4, 'Missed parallel axis theorem offset d^2 term', '2026-11-16 04:54:50')
ON CONFLICT (id) DO NOTHING;
INSERT INTO public.study_sessions (id, user_id, duration_seconds, subject, topic, chapter, question_num, is_correct, mistake_tag, score_delta, notes, timestamp)
VALUES ('7ffacac8-1949-5e2f-be2c-458430c91275', '96ede7d1-0ad8-5be9-a570-7d918d5d626e', 52.0, 'Chemistry', 'Thermodynamics', 'Thermodynamics', 1, TRUE, '', 4, 'Adiabatic expansion reversible vs irreversible work done', '2026-11-16 04:54:50')
ON CONFLICT (id) DO NOTHING;
INSERT INTO public.study_sessions (id, user_id, duration_seconds, subject, topic, chapter, question_num, is_correct, mistake_tag, score_delta, notes, timestamp)
VALUES ('aefbba6c-fd51-5908-98ef-b68303af33bf', '96ede7d1-0ad8-5be9-a570-7d918d5d626e', 110.5, 'Maths', 'Definite Integration', 'Definite Integration', 1, TRUE, '', 4, 'King''s property f(a+b-x) symmetry', '2026-11-16 04:54:50')
ON CONFLICT (id) DO NOTHING;
INSERT INTO public.study_sessions (id, user_id, duration_seconds, subject, topic, chapter, question_num, is_correct, mistake_tag, score_delta, notes, timestamp)
VALUES ('4c9cc5c7-0d5f-5e7d-b4e5-6202d3d6d7e7', '96ede7d1-0ad8-5be9-a570-7d918d5d626e', 180.0, 'Physics', 'Center of Mass', 'Center of Mass', 12, TRUE, '', 4, 'Solved using impulse equation', '2026-11-16 04:54:58')
ON CONFLICT (id) DO NOTHING;
INSERT INTO public.study_sessions (id, user_id, duration_seconds, subject, topic, chapter, question_num, is_correct, mistake_tag, score_delta, notes, timestamp)
VALUES ('ae611974-00e8-5955-83a0-c8ad702267cb', '96ede7d1-0ad8-5be9-a570-7d918d5d626e', 95.0, 'Chemistry', 'Chemical Equilibrium', 'Chemical Equilibrium', 5, FALSE, 'Calculation Mistake', -1, 'Forgot to square the concentration term', '2026-11-16 04:54:58')
ON CONFLICT (id) DO NOTHING;

-- 4. Insert CBT Results
INSERT INTO public.cbt_results (id, user_id, test_id, title, mode, subject, chapter, total_questions, score, max_score, accuracy, time_spent, answers_json, analytics_json, completed_at)
VALUES ('5a8391c7-3ea0-5ab6-98b7-e731881d5e2d', '96ede7d1-0ad8-5be9-a570-7d918d5d626e', 'cbt_mock_001', 'JEE Advanced 2025 Paper-1 Full Mock', 'advanced', 'Full', '', 54, 248, 360, 82.5, 10800, '[]'::jsonb, '{"testId": "cbt_mock_001", "title": "JEE Advanced 2025 Paper-1 Full Mock", "score": 248, "maxScore": 360, "accuracy": 82.5, "date": "2026-11-14T14:30:00Z", "breakdown": {"Physics": 84, "Chemistry": 88, "Maths": 76}}'::jsonb, '2026-11-16 04:54:50')
ON CONFLICT (id) DO NOTHING;
INSERT INTO public.cbt_results (id, user_id, test_id, title, mode, subject, chapter, total_questions, score, max_score, accuracy, time_spent, answers_json, analytics_json, completed_at)
VALUES ('aaaa3ddc-40ec-5cce-9f70-494d258bf87a', '96ede7d1-0ad8-5be9-a570-7d918d5d626e', 'offline_drill_01', 'Offline Rapid Revision CBT', 'advanced', 'Full', '', 30, 88, 120, 73.33, 3600, '[{"q": 1, "ans": "B"}]'::jsonb, '{"timePerQ": 120}'::jsonb, '2026-11-16 04:54:58')
ON CONFLICT (id) DO NOTHING;

COMMIT;
-- End of Migration Dump