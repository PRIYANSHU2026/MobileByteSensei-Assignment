# Supabase Integration Setup Guide

This guide will help you integrate Supabase with the Instagram Reels Analyzer to automatically store analyzed reel data.

## Prerequisites

- A Supabase account ([Create one here](https://supabase.com))
- Python 3.8+ installed
- The project cloned and ready

## Step 1: Create a Supabase Project

1. Go to [Supabase Dashboard](https://app.supabase.com)
2. Click "New Project"
3. Fill in the details:
   - **Name**: Instagram Reels Analyzer (or your preferred name)
   - **Database Password**: Choose a strong password
   - **Region**: Select the closest region
4. Click "Create new project" and wait for it to initialize (~2 minutes)

## Step 2: Set Up the Database Schema

1. In your Supabase project dashboard, go to **SQL Editor** (left sidebar)
2. Click "New Query"
3. Copy and paste the entire contents of `supabase_schema.sql` file
4. Click "Run" to execute the SQL commands

This will create:
- `instagram_reels` table - stores reel metadata and AI analysis
- `reel_comments` table - stores comments for each reel
- Indexes for faster queries
- Row Level Security policies
- A useful view `reels_with_comments` for querying data

## Step 3: Get Your Supabase Credentials

1. In your Supabase project dashboard, go to **Settings** → **API**
2. Copy the following values:
   - **Project URL** (looks like: `https://xxxxx.supabase.co`)
   - **anon public** key (under "Project API keys")

## Step 4: Configure Environment Variables

1. In the `MobileByteSensei-Assignment` folder, create a `.env` file:
   ```bash
   cp .env.example .env
   ```

2. Edit the `.env` file and add your Supabase credentials:
   ```env
   # Supabase Configuration
   SUPABASE_URL=https://your-project.supabase.co
   SUPABASE_KEY=your-anon-public-key-here

   # Instagram Credentials (Optional)
   INSTA_USER=your_instagram_username
   INSTA_PASS=your_instagram_password

   # Mistral AI API Key
   MISTRAL_API_KEY=your_mistral_api_key
   ```

## Step 5: Install Dependencies

```bash
cd MobileByteSensei-Assignment
pip install -r requirements.txt
```

This will install:
- `supabase` - Python client for Supabase
- `python-dotenv` - For loading environment variables
- All other existing dependencies

## Step 6: Test the Integration

### Option 1: Using the API

1. Start the Flask API:
   ```bash
   python api.py
   ```

2. You should see:
   ```
   ✓ Supabase client initialized successfully
   ```

3. Make a test request:
   ```bash
   curl -X POST http://localhost:5001/api/analyze \
     -H "Content-Type: application/json" \
     -d '{"target": "@instagram_profile", "max_reels": 2, "scraping_method": "instaloader"}'
   ```

4. Check your Supabase dashboard → Table Editor → `instagram_reels` to see the data!

### Option 2: Using the Streamlit App

1. Start the Streamlit app:
   ```bash
   streamlit run app.py
   ```

2. Enter a profile, hashtag, or URL and click "Analyze Reels"

3. Data will be automatically saved to Supabase

## Step 7: Verify Data in Supabase

1. Go to **Table Editor** in your Supabase dashboard
2. Click on `instagram_reels` table
3. You should see your analyzed reels with:
   - Reel metadata (caption, creator, likes, views)
   - AI analysis (summary, sentiment, categories)
   - Embeddings for similarity search
   - Upload date

4. Click on `reel_comments` table to see the comments

5. Try the view:
   ```sql
   SELECT * FROM reels_with_comments LIMIT 10;
   ```

## How It Works

### Automatic Data Storage

When you analyze reels:

1. **Scraping**: The app scrapes Instagram reel data
2. **AI Analysis**: Mistral AI analyzes the content
3. **Embedding Generation**: Creates vector embeddings
4. **Auto-Save**: Automatically saves to Supabase using `save_to_supabase()` function
5. **Upsert Logic**: Updates existing reels or inserts new ones

### Data Flow

```
Instagram → Scraper → AI Analysis → Supabase Database
                                   ↓
                         [instagram_reels table]
                         [reel_comments table]
```

## Querying Your Data

### Example Queries in Supabase SQL Editor

1. **Get all reels with sentiment analysis:**
   ```sql
   SELECT reel_id, caption, sentiment, ai_summary, likes, views
   FROM instagram_reels
   ORDER BY created_at DESC;
   ```

2. **Find reels by category:**
   ```sql
   SELECT * FROM instagram_reels
   WHERE 'Comedy' = ANY(category);
   ```

3. **Get top performing reels:**
   ```sql
   SELECT reel_id, creator_username, caption, likes, views
   FROM instagram_reels
   ORDER BY likes DESC
   LIMIT 10;
   ```

4. **Reels with their comments:**
   ```sql
   SELECT * FROM reels_with_comments
   WHERE creator_username = 'specific_user';
   ```

5. **Sentiment distribution:**
   ```sql
   SELECT sentiment, COUNT(*) as count
   FROM instagram_reels
   GROUP BY sentiment;
   ```

## Using the Data

### Python Client Example

```python
from supabase import create_client
import os
from dotenv import load_dotenv

load_dotenv()

supabase = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_KEY")
)

# Get all reels
response = supabase.table("instagram_reels").select("*").execute()
reels = response.data

# Filter by sentiment
positive_reels = supabase.table("instagram_reels")\
    .select("*")\
    .eq("sentiment", "Positive")\
    .execute()

# Get reels with high engagement
popular_reels = supabase.table("instagram_reels")\
    .select("*")\
    .gte("likes", 1000)\
    .execute()
```

## Troubleshooting

### "Supabase credentials not found"
- Make sure `.env` file exists in the project root
- Verify `SUPABASE_URL` and `SUPABASE_KEY` are set correctly
- Restart the application after adding credentials

### "Failed to initialize Supabase client"
- Check if your Supabase project URL is correct
- Verify the API key is the **anon public** key, not the service role key
- Ensure your Supabase project is active

### "Error saving to Supabase"
- Check if the database schema was created correctly
- Verify Row Level Security policies allow inserts
- Check Supabase logs in Dashboard → Logs

### Data not appearing
- Check the console for "✓ Saved reel..." messages
- Verify the reel_id is unique
- Check Supabase Table Editor to confirm data

## Advanced Features

### Real-time Subscriptions

You can set up real-time listeners to react when new reels are added:

```python
def handle_new_reel(payload):
    print(f"New reel: {payload['new']['reel_id']}")

supabase.table("instagram_reels")\
    .on("INSERT", handle_new_reel)\
    .subscribe()
```

### Vector Search with Embeddings

Use the embeddings for similarity search:

```python
# Find similar reels based on embeddings
# (Requires pgvector extension - enable in Supabase Dashboard → Database → Extensions)
```

### API Access

Your data is accessible via REST API:
```
GET https://your-project.supabase.co/rest/v1/instagram_reels
Authorization: Bearer your-anon-key
apikey: your-anon-key
```

## Security Best Practices

1. **Never commit `.env` file** - It's in `.gitignore` by default
2. **Use anon key for client-side** - Service role key has full access
3. **Configure RLS policies** - Adjust Row Level Security based on your needs
4. **Rotate keys regularly** - Generate new API keys periodically
5. **Monitor usage** - Check Supabase dashboard for unusual activity

## Next Steps

- Set up Supabase authentication for user-specific data
- Create custom views and functions for complex queries
- Build a dashboard using the stored data
- Set up scheduled jobs for automatic scraping
- Export data for machine learning models

## Support

- [Supabase Documentation](https://supabase.com/docs)
- [Supabase Discord](https://discord.supabase.com)
- [Project Issues](https://github.com/your-repo/issues)
