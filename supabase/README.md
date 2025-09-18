# Supabase Database Setup

This directory contains the database configuration for the At The Table app.

## Database Schema

### Tables:
- **bills** - Bill details, creator, link token
- **participants** - People in the bill, payer flag  
- **items** - Bill items (food, drinks, surcharges)
- **claims** - Exclusive claims of items
- **shared_members** - Participants in shared pools
- **submissions** - Participant confirmation status

## Setup Steps

1. Create Supabase project at https://supabase.com
2. Get project URL and API keys
3. Run migration scripts
4. Set up Row Level Security (RLS)
5. Configure environment variables

## Environment Variables Needed

```env
SUPABASE_URL=your_supabase_project_url
SUPABASE_ANON_KEY=your_supabase_anon_key
SUPABASE_SERVICE_ROLE_KEY=your_supabase_service_role_key
```
