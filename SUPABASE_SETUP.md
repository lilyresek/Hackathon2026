# ODMAP login + saved lists — Supabase setup

ODMAP now has email/password login and syncs each user's saved prescription
list to their account. This takes about 5 minutes and is free.

## 1. Create a Supabase project
1. Go to https://supabase.com and sign up (free, no card).
2. Click **New project**. Pick any name and a database password (you won't need
   the DB password for ODMAP — just don't lose it).
3. Wait ~1 minute for it to provision.

## 2. Create the table
1. In your project, open **SQL Editor** (left sidebar) > **New query**.
2. Open `supabase_setup.sql` from this folder, copy all of it, paste, and click **Run**.
   This creates a `saved_lists` table with Row Level Security so each user can
   only see their own list.

## 3. Get your keys
1. Go to **Project Settings** (gear icon) > **API**.
2. Copy two values:
   - **Project URL** (looks like `https://abcd1234.supabase.co`)
   - **anon public** key (a long string under "Project API keys")

   The anon key is designed to be used in browser code — it is safe to put in
   the HTML. Row Level Security is what actually protects the data.

## 4. Paste them into ODMAP
Open `odmap_v6.html`, find this block near the top of the `<script>`:

```js
const SUPABASE_URL  = "YOUR_SUPABASE_URL";
const SUPABASE_ANON = "YOUR_SUPABASE_ANON_KEY";
```

Replace the two placeholder strings with your Project URL and anon key. Save.

## 5. (Optional) turn off email confirmation for a smoother demo
By default Supabase emails a confirmation link on sign-up, so a new account
can't log in until the user clicks it. For a hackathon demo you can disable this:
- **Authentication** > **Providers** (or **Sign In / Providers**) > **Email** >
  turn **Confirm email** off.

With it off, sign-up logs the user straight in.

## That's it
Open `odmap_v6.html`, click **Log in** (top bar), create an account, and add
drugs to your Saved List. Log out and back in on any machine — your list follows
your account.

If Supabase isn't configured, ODMAP still runs fine; the saved list just stays
local to that browser session and the login button explains what to add.
