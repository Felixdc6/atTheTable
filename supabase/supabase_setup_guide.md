# Supabase Setup Guide

Follow these steps to set up Supabase for the At The Table app.

## Step 1: Create Supabase Project

1. Go to [supabase.com](https://supabase.com)
2. Sign up or log in
3. Click "New Project"
4. Choose your organization
5. Enter project details:
   - **Name**: `at-the-table` (or any name you prefer)
   - **Database Password**: Create a strong password (save it!)
   - **Region**: Choose closest to your location
6. Click "Create new project"
7. Wait for the project to be created (2-3 minutes)

## Step 2: Get Your Credentials

1. Go to **Settings** → **API** in your Supabase dashboard
2. Copy these values:
   - **Project URL** (looks like: `https://your-project-id.supabase.co`)
   - **anon public key** (starts with `eyJ...`)
   - **service_role secret key** (starts with `eyJ...`)

## Step 3: Update Environment Variables

Add these to your `env/config.env` file:

```env
# Supabase Configuration
SUPABASE_URL=https://your-project-id.supabase.co
SUPABASE_ANON_KEY=your_anon_key_here
SUPABASE_SERVICE_ROLE_KEY=your_service_role_key_here
```

## Step 4: Create Database Schema

1. Go to **SQL Editor** in your Supabase dashboard
2. Click "New Query"
3. Copy the entire contents of `supabase/schema.sql`
4. Paste it into the SQL editor
5. Click "Run" to execute the schema

## Step 5: Test the Connection

Run the test script:

```bash
python test_supabase.py
```

## Troubleshooting

### "Tables not found" error
- Make sure you ran the schema.sql file in Supabase SQL Editor
- Check that all tables were created successfully

### "Invalid API key" error
- Verify your API keys are correct
- Make sure you copied the full key (they're very long)

### "Connection refused" error
- Check your SUPABASE_URL is correct
- Make sure the project is fully created and running

### "Permission denied" error
- Use the service_role key for database operations
- The anon key has limited permissions

## Next Steps

Once Supabase is working:
1. Test the API endpoints
2. Create sample data
3. Set up the frontend
4. Connect everything together
