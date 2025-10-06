#!/usr/bin/env python3
"""
Quick Test Script - Test Supabase saving with a single reel
This bypasses Instagram rate limiting by using direct reel URLs
"""

import sys
from supabase_client import supabase_manager
from datetime import datetime

print("="*60)
print("Quick Test - Supabase Integration")
print("="*60)

# Create sample test data (mimics scraped reel data)
test_reel = {
    "reel_id": f"test_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
    "Reel_link": "https://www.instagram.com/reel/test123/",
    "caption": "This is a test reel to verify Supabase integration works correctly.",
    "creator": {
        "username": "test_user",
        "profile": "https://www.instagram.com/test_user/"
    },
    "ai_summary": "Test summary for verification",
    "category": ["Test", "Demo"],
    "likes": 100,
    "views": 500,
    "sentiment": "Positive",
    "top_comment_summary": "Test comments summary",
    "embeddings": [0.1, 0.2, 0.3, 0.4, 0.5],
    "top_comments": [
        {
            "user": "commenter1",
            "comment": "Great test!",
            "timestamp": datetime.now().isoformat()
        }
    ]
}

print("\n📊 Test Data Created:")
print(f"  Reel ID: {test_reel['reel_id']}")
print(f"  Caption: {test_reel['caption'][:50]}...")
print(f"  Likes: {test_reel['likes']}")
print(f"  Views: {test_reel['views']}")

print("\n💾 Saving to Supabase...")

try:
    # Save to Supabase
    result = supabase_manager.save_reel(test_reel)
    
    if result:
        print("\n✅ SUCCESS! Test data saved to Supabase!")
        print("\n🔍 Verification:")
        print("  1. Go to: https://supabase.com/dashboard/project/fhpejjuylcjcefciheence")
        print("  2. Click 'Table Editor'")
        print("  3. Select 'reels' table")
        print(f"  4. Look for reel_id: {test_reel['reel_id']}")
        
        print("\n✨ Next Steps:")
        print("  Now that Supabase is working, you can scrape real reels:")
        print("  python app_cli.py --cli --target @natgeo --max-reels 1 --save-supabase")
        print("\n" + "="*60)
    else:
        print("\n❌ Failed to save to Supabase")
        print("Check that you've run SUPABASE_SCHEMA.sql to create the table")
        
except Exception as e:
    print(f"\n❌ Error: {str(e)}")
    print("\nTroubleshooting:")
    print("  1. Make sure you've run SUPABASE_SCHEMA.sql")
    print("  2. Check internet connection")
    print("  3. Verify supabase_client.py has correct credentials")
