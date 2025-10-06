"""
yt-dlp integration module for Instagram Reels Analyzer
Handles video download from CDN links and Instagram URLs
"""

import yt_dlp
import os
from typing import Optional, Dict
import json

class YTDLPDownloader:
    """Manage video downloads using yt-dlp"""
    
    def __init__(self, output_dir: str = "downloads"):
        """
        Initialize yt-dlp downloader
        
        Args:
            output_dir: Directory to save downloaded videos
        """
        self.output_dir = output_dir
        
        # Create output directory if it doesn't exist
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
    
    def get_video_info(self, url: str) -> Optional[Dict]:
        """
        Get video information without downloading
        
        Args:
            url: Instagram reel URL or CDN link
            
        Returns:
            Dictionary with video information or None if failed
        """
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'extract_flat': False,
        }
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                
                return {
                    'title': info.get('title', ''),
                    'uploader': info.get('uploader', ''),
                    'duration': info.get('duration', 0),
                    'view_count': info.get('view_count', 0),
                    'like_count': info.get('like_count', 0),
                    'description': info.get('description', ''),
                    'thumbnail': info.get('thumbnail', ''),
                    'url': info.get('url', ''),
                    'formats': [
                        {
                            'format_id': f.get('format_id'),
                            'url': f.get('url'),
                            'ext': f.get('ext'),
                            'quality': f.get('height', 0),
                            'filesize': f.get('filesize', 0)
                        }
                        for f in info.get('formats', [])
                    ]
                }
        except Exception as e:
            print(f"Error getting video info: {str(e)}")
            return None
    
    def download_video(self, url: str, output_filename: Optional[str] = None) -> Optional[str]:
        """
        Download video from Instagram or CDN link
        
        Args:
            url: Instagram reel URL or CDN link
            output_filename: Custom filename (without extension)
            
        Returns:
            Path to downloaded file or None if failed
        """
        if output_filename:
            output_path = os.path.join(self.output_dir, f"{output_filename}.%(ext)s")
        else:
            output_path = os.path.join(self.output_dir, "%(id)s.%(ext)s")
        
        ydl_opts = {
            'format': 'best',
            'outtmpl': output_path,
            'quiet': False,
            'no_warnings': False,
        }
        
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                
                # Get the actual downloaded filename
                filename = ydl.prepare_filename(info)
                
                print(f"✓ Downloaded video to: {filename}")
                return filename
                
        except Exception as e:
            print(f"✗ Error downloading video: {str(e)}")
            return None
    
    def get_best_video_url(self, url: str) -> Optional[str]:
        """
        Get the best quality direct video URL without downloading
        
        Args:
            url: Instagram reel URL
            
        Returns:
            Direct video URL or None if failed
        """
        try:
            info = self.get_video_info(url)
            
            if not info or not info.get('formats'):
                return None
            
            # Find the best quality video format
            video_formats = [
                f for f in info['formats'] 
                if f.get('ext') == 'mp4' and f.get('quality', 0) > 0
            ]
            
            if not video_formats:
                # Fallback to any format with a URL
                video_formats = [f for f in info['formats'] if f.get('url')]
            
            if video_formats:
                # Sort by quality (height) descending
                best_format = max(video_formats, key=lambda x: x.get('quality', 0))
                return best_format.get('url')
            
            return None
            
        except Exception as e:
            print(f"Error getting best video URL: {str(e)}")
            return None
    
    def download_reel_batch(self, reels: list, use_reel_id: bool = True) -> Dict[str, str]:
        """
        Download multiple reels
        
        Args:
            reels: List of reel dictionaries with 'Reel_link' and 'reel_id'
            use_reel_id: Use reel_id as filename
            
        Returns:
            Dictionary mapping reel_id to downloaded file path
        """
        downloads = {}
        
        for reel in reels:
            reel_id = reel.get('reel_id', '')
            reel_link = reel.get('Reel_link', '')
            
            if not reel_link:
                print(f"✗ Skipping reel {reel_id}: No video link")
                continue
            
            filename = reel_id if use_reel_id else None
            
            try:
                downloaded_path = self.download_video(reel_link, filename)
                
                if downloaded_path:
                    downloads[reel_id] = downloaded_path
                    
            except Exception as e:
                print(f"✗ Failed to download reel {reel_id}: {str(e)}")
        
        print(f"\n{'='*50}")
        print(f"Download Summary:")
        print(f"  Total reels: {len(reels)}")
        print(f"  Successfully downloaded: {len(downloads)}")
        print(f"  Failed: {len(reels) - len(downloads)}")
        print(f"{'='*50}\n")
        
        return downloads
    
    def extract_cdn_link(self, instagram_url: str) -> Optional[str]:
        """
        Extract direct CDN link from Instagram reel URL
        
        Args:
            instagram_url: Instagram reel URL
            
        Returns:
            Direct CDN video link or None if failed
        """
        try:
            info = self.get_video_info(instagram_url)
            
            if info and info.get('url'):
                return info['url']
            
            # Try to get from formats
            if info and info.get('formats'):
                for fmt in info['formats']:
                    if fmt.get('url') and 'cdninstagram' in fmt['url']:
                        return fmt['url']
            
            return None
            
        except Exception as e:
            print(f"Error extracting CDN link: {str(e)}")
            return None

# Create a global instance
ytdlp_downloader = YTDLPDownloader()
