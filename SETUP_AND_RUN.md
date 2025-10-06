# 🚀 Complete Setup and Run Guide

## Step-by-Step Installation and Execution

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Internet connection

---

## 📦 Step 1: Install Dependencies

Open terminal/command prompt in the `MobileByteSensei-Assignment` folder and run:

```bash
# Navigate to project folder
cd MobileByteSensei-Assignment

# Install all required packages
pip install -r requirements.txt
```

**Note:** If you encounter errors, try:
```bash
# For Windows
pip install --upgrade pip
pip install -r requirements.txt

# For Mac/Linux
pip3 install --upgrade pip
pip3 install -r requirements.txt
```

---

## 🗄️ Step 2: Setup Supabase Database

### Option A: Use Existing Configuration (Recommended)
The project is already configured with Supabase credentials. Just create the table:

1. Go to your Supabase project: https://supabase.com/dashboard/project/fhpejjuylcjcefciheence
2. Click on "SQL Editor" in the left sidebar
3. Copy and paste the entire contents of `SUPABASE_SCHEMA.sql`
4. Click "Run" to create the `reels` table

### Option B: Use Your Own Supabase Project
1. Create a new Supabase project at https://supabase.com
2. Get your project URL and service_role key
3. Edit `supabase_client.py` and update:
```python
SUPABASE_URL = "your_project_url"
SUPABASE_KEY = "your_service_role_key"
```
4. Run the SQL from `SUPABASE_SCHEMA.sql` in your SQL Editor

---

## ▶️ Step 3: Run the Scraper

### Method 1: CLI Mode (Simplest - Recommended)

```bash
# Basic scraping with Supabase save
python app_cli.py --cli --target @instagram --max-reels 5 --save-supabase

# With CDN link extraction
python app_cli.py --cli --target @instagram --max-reels 5 --save-supabase --use-ytdlp

# Save to JSON file as well
python app_cli.py --cli --target @instagram --max-reels 5 --save-supabase --output results.json
```

### Method 2: Using Flask API

```bash
# Terminal 1: Start the API server
python api.py

# Terminal 2: Make a request
curl -X POST http://localhost:5001/api/analyze \
  -H "Content-Type: application/json" \
  -d '{"target": "@instagram", "max_reels": 5, "save_to_supabase": true, "use_ytdlp": true}'
```

### Method 3: Streamlit UI

```bash
streamlit run app.py
```
Then open http://localhost:8501 in your browser

---

## ✅ Quick Test Command

Run this to test everything:

```bash
python app_cli.py --cli --target @instagram --max-reels 3 --save-supabase --output test_results.json
```

This will:
- ✅ Scrape 3 reels from @instagram
- ✅ Save data to Supabase
- ✅ Save data to test_results.json
- ✅ Display progress in terminal

---

## 🔍 Verify Data in Supabase

1. Go to Supabase Dashboard
2. Click "Table Editor"
3. Select "reels" table
4. You should see your scraped data!

Or run this SQL query:
```sql
SELECT * FROM reels ORDER BY scraped_at DESC LIMIT 10;
```

---

## 📊 Example Commands

### Scrape from Different Sources

```bash
# From a username
python app_cli.py --cli --target @username --max-reels 10 --save-supabase

# From a hashtag
python app_cli.py --cli --target "#funny" --max-reels 10 --save-supabase

# From a direct URL
python app_cli.py --cli --target "https://www.instagram.com/reel/ABC123/" --save-supabase
```

### Use Different Methods

```bash
# Using Instaloader (default, more reliable)
python app_cli.py --cli --target @username --method instaloader --save-supabase

# Using Selenium (browser-based)
python app_cli.py --cli --target @username --method selenium --save-supabase
```

---

## 🛠️ Troubleshooting

### Issue: "Module not found"
**Solution:**
```bash
pip install -r requirements.txt --upgrade
```

### Issue: "torch installation failed"
**Solution:** Install torch separately:
```bash
# For CPU only (smaller, faster)
pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu

# Then install remaining dependencies
pip install -r requirements.txt
```

### Issue: "Supabase connection error"
**Solution:**
1. Check internet connection
2. Verify Supabase URL in `supabase_client.py`
3. Make sure the `reels` table exists (run SUPABASE_SCHEMA.sql)

### Issue: "No reels found"
**Solution:**
1. Try a different public profile (e.g., @instagram, @natgeo)
2. Make sure the account/hashtag is public
3. Wait a few minutes and try again (rate limiting)

### Issue: "Instagram login failed"
**Solution:**
- Use `instaloader` method instead of `selenium`
- Update credentials in `api.py` if using your own account
- Try without login using public profiles only

---

## 📝 Complete Working Example

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Test with a simple command
python app_cli.py --cli --target @natgeo --max-reels 3 --save-supabase --output my_results.json

# 3. Check the output
# - Look at my_results.json file
# - Check Supabase dashboard for data
# - Terminal will show progress and summary
```

---

## 🎯 Expected Output

When you run the command, you should see:

```
============================================================
Instagram Reels Analyzer - CLI Mode
============================================================

Scraping method: Instaloader
Target: @natgeo
Max reels: 3
Save to Supabase: True
Extract CDN links: False

------------------------------------------------------------
Fetching profile: natgeo
Processing reel 1 of 3

[1/3] Analyzing reel: ABC123
  ✓ Caption: Beautiful landscape...
  ✓ Likes: 45,678 | Views: 123,456
  ✓ Sentiment: Positive
  ✓ Categories: Nature

... (more reels)

==================================================
Supabase Storage Summary:
  Total reels: 3
  Successfully saved: 3
  Failed: 0
==================================================

💾 Saving results to my_results.json...
✓ Results saved to my_results.json

============================================================
SUMMARY
============================================================
Total reels analyzed: 3
Saved to Supabase: Yes
Output file: my_results.json
============================================================
```

---

## 🔄 Automated Scraping (Optional)

Create a script `auto_scrape.bat` (Windows) or `auto_scrape.sh` (Mac/Linux):

**Windows (auto_scrape.bat):**
```batch
@echo off
cd /d "%~dp0"
python app_cli.py --cli --target @instagram --max-reels 10 --save-supabase --output daily_scrape.json
```

**Mac/Linux (auto_scrape.sh):**
```bash
#!/bin/bash
cd "$(dirname "$0")"
python app_cli.py --cli --target @instagram --max-reels 10 --save-supabase --output daily_scrape.json
```

Run it:
```bash
# Windows
auto_scrape.bat

# Mac/Linux
chmod +x auto_scrape.sh
./auto_scrape.sh
```

---

## 📞 Need Help?

1. ✅ Check this guide first
2. ✅ Read error messages carefully
3. ✅ Verify all dependencies are installed
4. ✅ Make sure Supabase table is created
5. ✅ Try with a simple public profile first (@instagram, @natgeo)

---

## 🎉 Success Checklist

After running, verify:
- [ ] Terminal shows "Successfully saved: X" message
- [ ] JSON file created (if --output specified)
- [ ] Data visible in Supabase dashboard
- [ ] No error messages in terminal

**You're all set! Happy scraping! 🚀**
