"""
Supabase integration module for Instagram Reels Analyzer
Handles connection and data storage to Supabase
"""

from supabase import create_client, Client
from typing import Dict, List, Optional
import json
from datetime import datetime

# Supabase Configuration - USE YOUR CREDENTIALS
SUPABASE_URL = "https://fhpejjuyljcefcihence.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImZocGVqanV5bGpjZWZjaWhlbmNlIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc1ODQ0ODEzNywiZXhwIjoyMDc0MDI0MTM3fQ.ziqq7eSpMw8jQs8MvAZvNhwYuMuEdEPXUu069DY3uqM"

class SupabaseManager:
    """Manage Supabase connections and operations"""
    
    def __init__(self):
        """Initialize Supabase client"""
        try:
            self.client: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
            self.table_name = "reels"
        except Exception as e:
            print(f"✗ Failed to initialize Supabase client: {str(e)}")
            raise
    
    def save_reel(self, reel_data: Dict) -> Optional[Dict]:
        """
        Save a single reel to Supabase
        
        Args:
            reel_data: Dictionary containing reel information
            
        Returns:
            Response from Supabase or None if failed
        """
        try:
            # Prepare data for insertion
            data = {
                "reel_id": reel_data.get("reel_id", ""),
                "reel_link": reel_data.get("Reel_link", ""),
                "caption": reel_data.get("caption", ""),
                "creator_username": reel_data.get("creator", {}).get("username", ""),
                "creator_profile": reel_data.get("creator", {}).get("profile", ""),
                "ai_summary": reel_data.get("ai_summary", ""),
                "category": json.dumps(reel_data.get("category", [])),
                "likes": reel_data.get("likes", 0),
                "views": reel_data.get("views", 0),
                "sentiment": reel_data.get("sentiment", ""),
                "top_comment_summary": reel_data.get("top_comment_summary", ""),
                "embeddings": json.dumps(reel_data.get("embeddings", [])),
                "top_comments": json.dumps(reel_data.get("top_comments", [])),
                "upload_date": reel_data.get("upload_date", ""),
                "scraped_at": datetime.utcnow().isoformat()
            }
            
            # Insert into Supabase
            response = self.client.table(self.table_name).insert(data).execute()
            
            print(f"✓ Saved reel {data['reel_id']} to Supabase")
            return response.data
            
        except Exception as e:
            print(f"✗ Error saving reel to Supabase: {str(e)}")
            return None
    
    def save_reels_batch(self, reels: List[Dict]) -> bool:
        """
        Save multiple reels to Supabase
        
        Args:
            reels: List of reel dictionaries
            
        Returns:
            True if all successful, False otherwise
        """
        success_count = 0
        
        for reel in reels:
            result = self.save_reel(reel)
            if result:
                success_count += 1
        
        print(f"\n{'='*50}")
        print(f"Supabase Storage Summary:")
        print(f"  Total reels: {len(reels)}")
        print(f"  Successfully saved: {success_count}")
        print(f"  Failed: {len(reels) - success_count}")
        print(f"{'='*50}\n")
        
        return success_count == len(reels)
    
    def get_reel_by_id(self, reel_id: str) -> Optional[Dict]:
        """
        Retrieve a reel by its ID
        
        Args:
            reel_id: The reel ID to search for
            
        Returns:
            Reel data or None if not found
        """
        try:
            response = self.client.table(self.table_name).select("*").eq("reel_id", reel_id).execute()
            
            if response.data:
                return response.data[0]
            return None
            
        except Exception as e:
            print(f"Error retrieving reel: {str(e)}")
            return None
    
    def get_all_reels(self, limit: int = 100) -> List[Dict]:
        """
        Retrieve all reels from Supabase
        
        Args:
            limit: Maximum number of reels to retrieve
            
        Returns:
            List of reel dictionaries
        """
        try:
            response = self.client.table(self.table_name).select("*").limit(limit).execute()
            return response.data
            
        except Exception as e:
            print(f"Error retrieving reels: {str(e)}")
            return []
    
    def delete_reel(self, reel_id: str) -> bool:
        """
        Delete a reel by its ID
        
        Args:
            reel_id: The reel ID to delete
            
        Returns:
            True if successful, False otherwise
        """
        try:
            self.client.table(self.table_name).delete().eq("reel_id", reel_id).execute()
            print(f"✓ Deleted reel {reel_id}")
            return True
            
        except Exception as e:
            print(f"✗ Error deleting reel: {str(e)}")
            return False
    
    def reel_exists(self, reel_id: str) -> bool:
        """
        Check if a reel already exists in the database
        
        Args:
            reel_id: The reel ID to check
            
        Returns:
            True if exists, False otherwise
        """
        try:
            response = self.client.table(self.table_name).select("reel_id").eq("reel_id", reel_id).execute()
            return len(response.data) > 0
            
        except Exception as e:
            print(f"Error checking reel existence: {str(e)}")
            return False


# Create a global instance
supabase_manager = SupabaseManager()
