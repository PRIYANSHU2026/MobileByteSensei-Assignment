#!/usr/bin/env python3
"""
Instagram Reels Analyzer - CLI Mode
Supports both Streamlit UI and Command Line Interface
"""

import sys
import argparse
import json
from typing import Optional
import os

# Import all necessary modules
from supabase_client import supabase_manager
from ytdlp_downloader import ytdlp_downloader

def run_cli_mode(args):
    """Run the analyzer in CLI mode"""
    print("="*60)
    print("Instagram Reels Analyzer - CLI Mode")
    print("="*60)
    
    # Import scraping functions
    if args.method == 'instaloader':
        from api import scrape_with_instaloader, analyze_reel_with_ai
        print(f"\nScraping method: Instaloader")
        print(f"Target: {args.target}")
        print(f"Max reels: {args.max_reels}")
        print(f"Save to Supabase: {args.save_supabase}")
        print(f"Extract CDN links: {args.use_ytdlp}")
        print("\n" + "-"*60)
        
        # Scrape reels
        reels = scrape_with_instaloader(args.target, max_reels=args.max_reels)
        
        if not reels:
            print("❌ No reels found!")
            return
        
        print(f"\n✓ Found {len(reels)} reels")
        
        # Analyze each reel
        results = []
        for i, reel in enumerate(reels, 1):
            print(f"\n[{i}/{len(reels)}] Analyzing reel: {reel.get('reel_id')}")
            
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
            
            # Extract CDN link if requested
            if args.use_ytdlp:
                print(f"  → Extracting CDN link...")
                instagram_url = f"https://www.instagram.com/reel/{full_result['reel_id']}/"
                cdn_link = ytdlp_downloader.extract_cdn_link(instagram_url)
                if cdn_link:
                    full_result["cdn_link"] = cdn_link
                    print(f"  ✓ CDN link extracted")
            
            results.append(full_result)
            
            # Print summary
            print(f"  ✓ Caption: {full_result['caption'][:50]}...")
            print(f"  ✓ Likes: {full_result['likes']:,} | Views: {full_result['views']:,}")
            print(f"  ✓ Sentiment: {full_result['sentiment']}")
            print(f"  ✓ Categories: {', '.join(full_result['category'])}")
        
        # Save to Supabase if requested
        if args.save_supabase:
            print("\n" + "="*60)
            print("Saving to Supabase...")
            print("="*60)
            supabase_manager.save_reels_batch(results)
        
        # Save to JSON file if output specified
        if args.output:
            print(f"\n💾 Saving results to {args.output}...")
            with open(args.output, 'w', encoding='utf-8') as f:
                json.dump(results, f, indent=2, ensure_ascii=False)
            print(f"✓ Results saved to {args.output}")
        
        # Print summary
        print("\n" + "="*60)
        print("SUMMARY")
        print("="*60)
        print(f"Total reels analyzed: {len(results)}")
        print(f"Saved to Supabase: {'Yes' if args.save_supabase else 'No'}")
        print(f"Output file: {args.output if args.output else 'None'}")
        print("="*60)
        
    elif args.method == 'selenium':
        from api import get_webdriver, login_to_instagram, scrape_instagram_reels, analyze_reel_with_ai
        
        print(f"\nScraping method: Selenium")
        print(f"Target: {args.target}")
        print(f"Max reels: {args.max_reels}")
        print(f"Use login: {args.use_login}")
        print(f"Save to Supabase: {args.save_supabase}")
        print(f"Extract CDN links: {args.use_ytdlp}")
        print("\n" + "-"*60)
        
        # Initialize browser
        driver = get_webdriver()
        if not driver:
            print("❌ Failed to initialize browser!")
            return
        
        try:
            # Login if requested
            if args.use_login:
                print("Logging in to Instagram...")
                login_success = login_to_instagram(driver)
                if not login_success:
                    print("⚠ Login failed, proceeding without login")
            
            # Scrape reels
            reels = scrape_instagram_reels(driver, args.target, max_reels=args.max_reels)
            
            if not reels:
                print("❌ No reels found!")
                return
            
            print(f"\n✓ Found {len(reels)} reels")
            
            # Analyze each reel
            results = []
            for i, reel in enumerate(reels, 1):
                print(f"\n[{i}/{len(reels)}] Analyzing reel: {reel.get('reel_id')}")
                
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
                
                # Extract CDN link if requested
                if args.use_ytdlp:
                    print(f"  → Extracting CDN link...")
                    instagram_url = f"https://www.instagram.com/reel/{full_result['reel_id']}/"
                    cdn_link = ytdlp_downloader.extract_cdn_link(instagram_url)
                    if cdn_link:
                        full_result["cdn_link"] = cdn_link
                        print(f"  ✓ CDN link extracted")
                
                results.append(full_result)
                
                # Print summary
                print(f"  ✓ Caption: {full_result['caption'][:50]}...")
                print(f"  ✓ Likes: {full_result['likes']:,} | Views: {full_result['views']:,}")
                print(f"  ✓ Sentiment: {full_result['sentiment']}")
                print(f"  ✓ Categories: {', '.join(full_result['category'])}")
            
            # Save to Supabase if requested
            if args.save_supabase:
                print("\n" + "="*60)
                print("Saving to Supabase...")
                print("="*60)
                supabase_manager.save_reels_batch(results)
            
            # Save to JSON file if output specified
            if args.output:
                print(f"\n💾 Saving results to {args.output}...")
                with open(args.output, 'w', encoding='utf-8') as f:
                    json.dump(results, f, indent=2, ensure_ascii=False)
                print(f"✓ Results saved to {args.output}")
            
            # Print summary
            print("\n" + "="*60)
            print("SUMMARY")
            print("="*60)
            print(f"Total reels analyzed: {len(results)}")
            print(f"Saved to Supabase: {'Yes' if args.save_supabase else 'No'}")
            print(f"Output file: {args.output if args.output else 'None'}")
            print("="*60)
            
        finally:
            driver.quit()

def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='Instagram Reels Analyzer - CLI Mode',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Scrape reels using Instaloader and save to Supabase
  python app_cli.py --cli --target @instagram --max-reels 5 --save-supabase

  # Scrape reels using Selenium with CDN extraction
  python app_cli.py --cli --target @username --method selenium --use-ytdlp

  # Save results to JSON file
  python app_cli.py --cli --target "#funny" --output results.json

  # Run Streamlit UI (default)
  python app_cli.py
        """
    )
    
    parser.add_argument(
        '--cli',
        action='store_true',
        help='Run in CLI mode instead of Streamlit UI'
    )
    
    parser.add_argument(
        '--target',
        type=str,
        help='Instagram target: @username, #hashtag, or URL'
    )
    
    parser.add_argument(
        '--max-reels',
        type=int,
        default=10,
        help='Maximum number of reels to analyze (default: 10)'
    )
    
    parser.add_argument(
        '--method',
        choices=['instaloader', 'selenium'],
        default='instaloader',
        help='Scraping method (default: instaloader)'
    )
    
    parser.add_argument(
        '--save-supabase',
        action='store_true',
        help='Save results to Supabase database'
    )
    
    parser.add_argument(
        '--use-ytdlp',
        action='store_true',
        help='Extract CDN links using yt-dlp'
    )
    
    parser.add_argument(
        '--use-login',
        action='store_true',
        default=True,
        help='Use Instagram login (Selenium only)'
    )
    
    parser.add_argument(
        '--output',
        type=str,
        help='Save results to JSON file'
    )
    
    args = parser.parse_args()
    
    # Check if CLI mode
    if args.cli:
        if not args.target:
            parser.error("--target is required in CLI mode")
        run_cli_mode(args)
    else:
        # Run Streamlit UI
        print("Starting Streamlit UI...")
        print("Note: Use --cli flag to run in command-line mode")
        print("Example: python app_cli.py --cli --target @username --max-reels 5")
        print("\nStarting Streamlit...")
        import subprocess
        subprocess.run(['streamlit', 'run', 'app.py'])

if __name__ == '__main__':
    main()
