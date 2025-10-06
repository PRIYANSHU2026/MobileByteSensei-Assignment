# Instagram Reels Analyzer - Complete Usage Guide

## 🚀 New Features Added

### 1. **Supabase Integration**
- Automatically saves scraped reel data to Supabase database
- Stores all metrics, AI analysis, and comments
- Includes analytics views for insights

### 2. **yt-dlp CDN Link Extraction**
- Extract direct CDN video URLs from Instagram reels
- Bypass Instagram's blob URLs for better video access
- Download videos using yt-dlp

### 3. **CLI Mode**
- Run the analyzer from command line without Streamlit UI
- Perfect for automation, cron jobs, and batch processing
- Save results to JSON files

---

## 📋 Table of Contents

1. [Installation](#installation)
2. [Supabase Setup](#supabase-setup)
3. [Configuration](#configuration)
4. [Usage Methods](#usage-methods)
5. [API Reference](#api-reference)
6. [Examples](#examples)
7. [Troubleshooting](#troubleshooting)

---

## 🔧 Installation

### 1. Install Dependencies

```bash
cd MobileByteSensei-Assignment
pip install -r requirements.txt
```

### 2. Verify Installation

```bash
python -c "import supabase; import yt_dlp; print('All dependencies installed!')"
```

---

## 🗄️ Supabase Setup

### Step 1: Create Supabase Project

1. Go to [https://supabase.com](https://supabase.com)
2. Create a new project
3. Note your project URL and API keys

### Step 2: Create Database Table

1. Open SQL Editor in Supabase Dashboard
2. Copy contents from `SUPABASE_SCHEMA.sql`
3. Execute the SQL to create the `reels` table

### Step 3: Configure Credentials

The credentials are already configured in `supabase_client.py`:
- **URL**: `https://fhpejjuylcjcefciheence.supabase.co`
- **Service Role Key**: Already set in the code

---

## ⚙️ Configuration

### Instagram Credentials

Edit `api.py` and `app.py` to update:

```python
INSTA_USER = "your_username"  # Your Instagram username
INSTA_PASS = "your_password"  # Your Instagram password
```

### Mistral AI API Key

The API key is already configured. If you need to change it:

```python
MISTRAL_API_KEY = "your_api_key_here"
```

---

## 🎯 Usage Methods

### Method 1: CLI Mode (Recommended for Automation)

#### Basic Usage

```bash
# Scrape reels and save to Supabase
python app_cli.py --cli --target @username --max-reels 10 --save-supabase

# Extract CDN links
python app_cli.py --cli --target @username --use-ytdlp --save-supabase

# Save to JSON file
python app_cli.py --cli --target "#funny" --output results.json

# Use Selenium method
python app_cli.py --cli --target @username --method selenium --use-login
```

#### Complete Example

```bash
python app_cli.py \
  --cli \
  --target @only_comedy_vid \
  --max-reels 5 \
  --method instaloader \
  --save-supabase \
  --use-ytdlp \
  --output my_results.json
```

### Method 2: Streamlit UI

```bash
# Run the web interface
streamlit run app.py

# Or using app_cli.py without --cli flag
python app_cli.py
```

Then open your browser to `http://localhost:8501`

### Method 3: Flask REST API

```bash
# Start the API server
python api.py
```

API will be available at `http://localhost:5001`

#### API Endpoints

**Health Check:**
```bash
curl http://localhost:5001/api/health
```

**Analyze Reels:**
```bash
curl -X POST http://localhost:5001/api/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "target": "@username",
    "max_reels": 10,
    "scraping_method": "instaloader",
    "save_to_supabase": true,
    "use_ytdlp": true
  }'
```

---

## 📚 API Reference

### CLI Arguments

| Argument | Type | Default | Description |
|----------|------|---------|-------------|
| `--cli` | flag | False | Enable CLI mode |
| `--target` | string | required | Instagram @username, #hashtag, or URL |
| `--max-reels` | int | 10 | Maximum number of reels to analyze |
| `--method` | choice | instaloader | Scraping method: `instaloader` or `selenium` |
| `--save-supabase` | flag | False | Save results to Supabase |
| `--use-ytdlp` | flag | False | Extract CDN links with yt-dlp |
| `--use-login` | flag | True | Use Instagram login (Selenium only) |
| `--output` | string | None | Save results to JSON file |

### REST API Parameters

```json
{
  "target": "@username or #hashtag or URL",
  "max_reels": 10,
  "use_login": true,
  "scraping_method": "instaloader",
  "save_to_supabase": true,
  "use_ytdlp": false
}
```

### Response Format

```json
{
  "status": "success",
  "count": 5,
  "saved_to_supabase": true,
  "results": [
    {
      "reel_id": "ABC123",
      "Reel_link": "https://instagram.com/reel/ABC123/",
      "cdn_link": "https://cdn.instagram.com/video.mp4",
      "caption": "Funny video...",
      "creator": {
        "username": "creator_name",
        "profile": "https://instagram.com/creator_name/"
      },
      "ai_summary": "A humorous video...",
      "category": ["Comedy", "Skits"],
      "likes": 12345,
      "views": 67890,
      "sentiment": "Funny",
      "top_comment_summary": "Users found it hilarious",
      "embeddings": [0.123, 0.456, ...],
      "top_comments": [
        {
          "user": "user1",
          "comment": "So funny! 😂",
          "timestamp": "2025-01-15T10:30:00Z"
        }
      ]
    }
  ]
}
```

---

## 💡 Examples

### Example 1: Batch Processing with CLI

```bash
#!/bin/bash
# Script to scrape multiple profiles

PROFILES=("@profile1" "@profile2" "@profile3")

for profile in "${PROFILES[@]}"; do
  echo "Processing $profile..."
  python app_cli.py \
    --cli \
    --target "$profile" \
    --max-reels 20 \
    --save-supabase \
    --use-ytdlp \
    --output "results_${profile//[@]/}.json"
  
  echo "Completed $profile"
  sleep 60  # Wait 60 seconds between profiles
done
```

### Example 2: Cron Job Setup

```bash
# Add to crontab (crontab -e)
# Run every day at 2 AM
0 2 * * * cd /path/to/MobileByteSensei-Assignment && python app_cli.py --cli --target @trending_account --max-reels 50 --save-supabase --use-ytdlp >> /var/log/reels_scraper.log 2>&1
```

### Example 3: Python Script Integration

```python
import subprocess
import json

def scrape_and_process(target, max_reels=10):
    """Scrape reels and process results"""
    
    # Run CLI command
    result = subprocess.run([
        'python', 'app_cli.py',
        '--cli',
        '--target', target,
        '--max-reels', str(max_reels),
        '--save-supabase',
        '--use-ytdlp',
        '--output', 'temp_results.json'
    ], capture_output=True, text=True)
    
    # Load results
    with open('temp_results.json', 'r') as f:
        data = json.load(f)
    
    # Process data
    for reel in data:
        print(f"Reel: {reel['reel_id']}")
        print(f"Likes: {reel['likes']:,}")
        print(f"Views: {reel['views']:,}")
        print(f"Sentiment: {reel['sentiment']}")
        print("-" * 50)
    
    return data

# Usage
results = scrape_and_process('@username', max_reels=5)
```

### Example 4: Query Supabase Data

```python
from supabase_client import supabase_manager

# Get all reels from a creator
creator_reels = supabase_manager.client.table('reels')\
    .select('*')\
    .eq('creator_username', 'username')\
    .execute()

# Get top reels by likes
top_reels = supabase_manager.client.table('reels')\
    .select('*')\
    .order('likes', desc=True)\
    .limit(10)\
    .execute()

# Get reels by category
comedy_reels = supabase_manager.client.table('reels')\
    .select('*')\
    .contains('category', ['Comedy'])\
    .execute()
```

---

## 🔍 Troubleshooting

### Issue: "Login failed"

**Solution:**
1. Check Instagram credentials in `api.py` and `app.py`
2. Instagram may require 2FA - use app-specific password
3. Try using `instaloader` method instead of `selenium`

### Issue: "No reels found"

**Solution:**
1. Ensure the profile/hashtag is public
2. Try with a different target
3. Check if Instagram is blocking requests (wait and retry)

### Issue: "Supabase connection error"

**Solution:**
1. Verify Supabase URL and API key in `supabase_client.py`
2. Check if table `reels` exists in Supabase
3. Run `SUPABASE_SCHEMA.sql` to create the table

### Issue: "yt-dlp extraction failed"

**Solution:**
1. Ensure `yt-dlp` is updated: `pip install --upgrade yt-dlp`
2. Some reels may have restrictions
3. Try without `--use-ytdlp` flag

### Issue: "Rate limiting / Too many requests"

**Solution:**
1. Reduce `--max-reels` number
2. Add delays between requests
3. Use Instagram login for higher rate limits
4. Spread out scraping over time

---

## 📊 Database Queries

### Useful SQL Queries for Supabase

```sql
-- Get top creators by total views
SELECT 
    creator_username,
    COUNT(*) as total_reels,
    SUM(views) as total_views,
    AVG(likes) as avg_likes
FROM reels
GROUP BY creator_username
ORDER BY total_views DESC
LIMIT 10;

-- Get reels by sentiment
SELECT sentiment, COUNT(*) as count
FROM reels
GROUP BY sentiment
ORDER BY count DESC;

-- Get reels scraped today
SELECT *
FROM reels
WHERE DATE(scraped_at) = CURRENT_DATE
ORDER BY views DESC;

-- Get most liked reels
SELECT 
    reel_id,
    caption,
    creator_username,
    likes,
    views
FROM reels
ORDER BY likes DESC
LIMIT 20;
```

---

## 🎉 Features Summary

✅ **Supabase Integration** - Automatic database storage  
✅ **yt-dlp CDN Links** - Direct video URL extraction  
✅ **CLI Mode** - Command-line automation  
✅ **REST API** - HTTP endpoints for integration  
✅ **Streamlit UI** - Interactive web interface  
✅ **AI Analysis** - Mistral AI-powered insights  
✅ **Dual Scraping** - Both Selenium and Instaloader  
✅ **Batch Processing** - Handle multiple targets  
✅ **JSON Export** - Save results to files  

---

## 📞 Support

For issues or questions:
1. Check this guide first
2. Review error messages carefully
3. Ensure all dependencies are installed
4. Verify configuration settings

---

**Happy Scraping! 🚀**
