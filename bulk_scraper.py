#!/usr/bin/env python3
"""
Bulk Instagram Reel Scraper
Scrape reels from multiple sources and save to Supabase
"""

import sys
import time
import argparse

# Import scraping functions directly
from api import scrape_with_instaloader, analyze_reel_with_ai
from supabase_client import supabase_manager

# EXPANDED List of profiles/hashtags to scrape (100+ sources)
# To get 10,000 reels: 100 sources × 100 reels each = 10,000 reels
TARGETS = [
    # Popular Profiles
    "@natgeo", "@nasa", "@9gag", "@bbcearth", "@instagram",
    "@therock", "@cristiano", "@kimkardashian", "@selenagomez", "@beyonce",
    "@taylorswift", "@arianagrande", "@justinbieber", "@nike", "@adidas",
    "@redbull", "@gopro", "@netflix", "@disney", "@marvel",
    "@starwars", "@spotify", "@playstation", "@xbox", "@apple",
    "@google", "@microsoft", "@amazon", "@tesla", "@spacex",
    
    # Comedy & Entertainment
    "@comedy", "@memezar", "@funnymemes", "@dankmemes", "@laugh",
    "@comedycentral", "@snl", "@trevornoah", "@theellenshow", "@jimmyfallon",
    "@stephencolbert", "@comedians", "@standup", "@jokes", "@humor",
    
    # Sports
    "@nba", "@nfl", "@fifa", "@uefa", "@premierleague",
    "@realmadrid", "@fcbarcelona", "@manchesterunited", "@liverpool", "@psg",
    "@leomessi", "@neymarjr", "@kylianmbappe", "@erlinghaaland", "@lebron",
    "@stephencurry", "@kobe", "@usainbolt", "@serena", "@rogerfederer",
    
    # Lifestyle & Fashion
    "@vogue", "@gq", "@gucci", "@chanel", "@louisvuitton",
    "@prada", "@dior", "@versace", "@balenciaga", "@fashion",
    "@style", "@ootd", "@streetstyle", "@mensfashion", "@womensfashion",
    
    # Travel & Nature
    "@beautifuldestinations", "@earthpix", "@wonderful_places", "@travelgram", "@wanderlust",
    "@travel", "@adventure", "@explore", "@mountains", "@ocean",
    "@sunset", "@wildlife", "@animalsofinstagram", "@dogs", "@cats",
    
    # Food & Restaurants
    "@foodnetwork", "@tasty", "@buzzfeedtasty", "@delish", "@foodie",
    "@yummy", "@instafood", "@cooking", "@chef", "@restaurant",
    
    # Tech & Innovation
    "@techcrunch", "@wired", "@verge", "@gadgets", "@technology",
    "@innovation", "@ai", "@robots", "@future", "@science",
    
    # Hashtags (High Volume)
    "#viral", "#trending", "#funny", "#comedy", "#memes",
    "#travel", "#nature", "#food", "#fashion", "#fitness",
    "#motivation", "#inspiration", "#love", "#life", "#happy",
    "#beautiful", "#art", "#music", "#dance", "#sports",
    "#technology", "#business", "#entrepreneur", "#success", "#goals",
    "#lifestyle", "#luxury", "#adventure", "#explore", "#wanderlust",
    "#photooftheday", "#instagood", "#picoftheday", "#instadaily", "#follow",
    "#reels", "#reelsinstagram", "#instareels", "#reelitfeelit", "#reelsvideo",
    "#explore", "#explorepage", "#fyp", "#foryou", "#foryoupage"
]

def bulk_scrape(targets, max_reels_per_target=5, method="instaloader", delay=60):
    """
    Scrape reels from multiple targets
    
    Args:
        targets: List of targets to scrape
        max_reels_per_target: Number of reels to scrape from each target
        method: 'instaloader' or 'selenium'
        delay: Delay in seconds between targets (to avoid rate limiting)
    """
    print("="*60)
    print("BULK INSTAGRAM REEL SCRAPER")
    print("="*60)
    print(f"\nTargets: {len(targets)}")
    print(f"Max reels per target: {max_reels_per_target}")
    print(f"Total potential reels: {len(targets) * max_reels_per_target}")
    print(f"Method: {method}")
    print(f"Delay between targets: {delay}s")
    print("="*60)
    
    total_scraped = 0
    failed_targets = []
    
    for i, target in enumerate(targets, 1):
        print(f"\n\n{'='*60}")
        print(f"[{i}/{len(targets)}] Processing: {target}")
        print("="*60)
        
        try:
            # Scrape reels
            reels = scrape_with_instaloader(target, max_reels=max_reels_per_target)
            
            if not reels:
                print(f"✗ No reels found for {target}")
                failed_targets.append(target)
                continue
            
            print(f"✓ Found {len(reels)} reels from {target}")
            
            # Analyze each reel with AI
            results = []
            for reel in reels:
                ai_analysis = analyze_reel_with_ai(reel)
                
                full_result = {
                    "reel_id": reel.get("reel_id", ""),
                    "Reel_link": reel.get("Reel_link", ""),
                    "caption": reel.get("caption", ""),
                    "creator": reel.get("creator", {}),
                    "ai_summary": ai_analysis.get("ai_summary", ""),
                    "category": ai_analysis.get("category", []),
                    "likes": reel.get("likes", 0),
                    "views": reel.get("views", 0),
                    "sentiment": ai_analysis.get("sentiment", ""),
                    "top_comment_summary": ai_analysis.get("top_comment_summary", ""),
                    "embeddings": ai_analysis.get("embeddings", []),
                    "top_comments": reel.get("top_comments", [])
                }
                results.append(full_result)
            
            # Save to Supabase
            if results:
                supabase_manager.save_reels_batch(results)
                total_scraped += len(results)
                print(f"✓ Saved {len(results)} reels to Supabase")
            
            # Wait before next target to avoid rate limiting
            if i < len(targets):
                print(f"\n⏳ Waiting {delay}s before next target...")
                time.sleep(delay)
                
        except Exception as e:
            print(f"✗ Error processing {target}: {str(e)}")
            failed_targets.append(target)
            continue
    
    # Final summary
    print("\n\n" + "="*60)
    print("BULK SCRAPING COMPLETE")
    print("="*60)
    print(f"Total reels scraped: {total_scraped}")
    print(f"Successful targets: {len(targets) - len(failed_targets)}/{len(targets)}")
    
    if failed_targets:
        print(f"\nFailed targets ({len(failed_targets)}):")
        for target in failed_targets:
            print(f"  - {target}")
    
    print("\n✓ All data saved to Supabase!")
    print("Check your dashboard: https://supabase.com/dashboard")
    print("="*60)

def main():
    parser = argparse.ArgumentParser(description='Bulk scrape Instagram reels from multiple sources')
    parser.add_argument('--targets', nargs='+', default=TARGETS,
                      help='List of targets to scrape (profiles or hashtags)')
    parser.add_argument('--max-reels', type=int, default=5,
                      help='Maximum reels per target (default: 5)')
    parser.add_argument('--method', choices=['instaloader', 'selenium'], default='instaloader',
                      help='Scraping method (default: instaloader)')
    parser.add_argument('--delay', type=int, default=60,
                      help='Delay between targets in seconds (default: 60)')
    parser.add_argument('--quick', action='store_true',
                      help='Quick mode: 3 reels per target, 30s delay')
    
    args = parser.parse_args()
    
    # Quick mode
    if args.quick:
        args.max_reels = 3
        args.delay = 30
        print("🚀 Quick mode enabled: 3 reels/target, 30s delay")
    
    # Start bulk scraping
    bulk_scrape(
        targets=args.targets,
        max_reels_per_target=args.max_reels,
        method=args.method,
        delay=args.delay
    )

if __name__ == "__main__":
    main()
