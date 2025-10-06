#!/usr/bin/env python3
"""
Quick test script to verify all dependencies and connections
Run this before using the main scraper
"""

import sys

print("="*60)
print("Testing Instagram Reels Analyzer Setup")
print("="*60)

# Test 1: Python version
print("\n[1/7] Checking Python version...")
if sys.version_info >= (3, 8):
    print(f"✓ Python {sys.version.split()[0]} detected")
else:
    print(f"✗ Python 3.8+ required, you have {sys.version}")
    sys.exit(1)

# Test 2: Core dependencies
print("\n[2/7] Checking core dependencies...")
try:
    import requests
    import selenium
    import instaloader
    print("✓ Core scraping libraries installed")
except ImportError as e:
    print(f"✗ Missing dependency: {e}")
    print("Run: pip install -r requirements.txt")
    sys.exit(1)

# Test 3: AI dependencies
print("\n[3/7] Checking AI/ML libraries...")
try:
    import torch
    import sentence_transformers
    print(f"✓ PyTorch and Sentence Transformers installed")
except ImportError as e:
    print(f"⚠ AI libraries not fully installed: {e}")
    print("Note: AI features may not work, but scraping will still function")

# Test 4: Database connection
print("\n[4/7] Testing Supabase connection...")
try:
    from supabase_client import supabase_manager
    # Try to access the client
    client = supabase_manager.client
    print("✓ Supabase client initialized")
    
    # Test connection by checking health
    try:
        response = client.table('reels').select("count", count='exact').limit(1).execute()
        print(f"✓ Supabase connection successful")
    except Exception as e:
        print(f"⚠ Supabase connection issue: {str(e)[:100]}")
        print("  Make sure you've run SUPABASE_SCHEMA.sql to create the 'reels' table")
except ImportError as e:
    print(f"✗ Supabase module error: {e}")
    sys.exit(1)

# Test 5: yt-dlp
print("\n[5/7] Checking yt-dlp...")
try:
    import yt_dlp
    from ytdlp_downloader import ytdlp_downloader
    print("✓ yt-dlp installed and module loaded")
except ImportError as e:
    print(f"✗ yt-dlp not installed: {e}")
    sys.exit(1)

# Test 6: Web frameworks
print("\n[6/7] Checking web frameworks...")
try:
    import streamlit
    import flask
    from flask_cors import CORS
    print("✓ Streamlit and Flask installed")
except ImportError as e:
    print(f"✗ Web framework missing: {e}")
    sys.exit(1)

# Test 7: Other utilities
print("\n[7/7] Checking utilities...")
try:
    import pandas
    import beautifulsoup4
    from webdriver_manager.chrome import ChromeDriverManager
    print("✓ All utility libraries installed")
except ImportError as e:
    print(f"⚠ Some utilities missing: {e}")
    print("  Most features will still work")

# Summary
print("\n" + "="*60)
print("SETUP VERIFICATION COMPLETE")
print("="*60)
print("\n✅ Your environment is ready!")
print("\nNext steps:")
print("1. Setup Supabase table (run SUPABASE_SCHEMA.sql)")
print("2. Run a test scrape:")
print("   python app_cli.py --cli --target @instagram --max-reels 2 --save-supabase")
print("\n" + "="*60)
