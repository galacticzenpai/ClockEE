# ClockEE Production Deployment & Edge Status Notes

## 1. Vercel Edge 402 Payment Required Advisory
- **Domain**: `https://clockee.vercel.app`
- **Observed Status**: HTTP 402: Payment Required
- **Root Cause**: The Vercel account or team project hosting `clockee.vercel.app` is currently paused or restricted due to account-level billing/usage limits on Vercel.
- **Resolution Steps for Account Owner**:
  1. Log in to [Vercel Dashboard](https://vercel.com/dashboard).
  2. Navigate to **Team Settings** > **Billing** or **Project Settings**.
  3. Verify payment method status, settle outstanding invoices or reactivate paused subscription tier.
  4. Once billing is settled, unpause or redeploy project `clockee` via `vercel --prod`.

## 2. Supabase Serverless & Backend Gateway Remediation
- **Status**: Operational (`api/index.py`).
- **Remediated Issues**:
  - **PostgreSQL 22P02 (UUID Format)**: Added `to_uuid()` deterministic uuid5 casting for non-UUID / guest usernames.
  - **PostgreSQL 23503 (Foreign Key)**: Dropped foreign key constraints referencing `auth.users(id)` from `cbt_results`, `student_states`, `study_sessions`, and `profiles` to enable unauthenticated / guest offline exam submissions without schema constraint violations.
  - **PostgreSQL 42501 (RLS)**: Added RLS bypass / fallback handling for backend operations and configured policies for `anon` and `authenticated` roles.
  - **Auth Route Aliases**: Added `/api/auth/session` and `/auth/session` aliases resolving HTTP 404s.
