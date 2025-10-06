-- Supabase Schema for Instagram Reels Analyzer
-- Create this table in your Supabase project

CREATE TABLE IF NOT EXISTS reels (
    id BIGSERIAL PRIMARY KEY,
    reel_id TEXT UNIQUE NOT NULL,
    reel_link TEXT,
    caption TEXT,
    creator_username TEXT,
    creator_profile TEXT,
    ai_summary TEXT,
    category JSONB DEFAULT '[]'::jsonb,
    likes INTEGER DEFAULT 0,
    views INTEGER DEFAULT 0,
    sentiment TEXT,
    top_comment_summary TEXT,
    embeddings JSONB DEFAULT '[]'::jsonb,
    top_comments JSONB DEFAULT '[]'::jsonb,
    upload_date TEXT,
    scraped_at TIMESTAMP DEFAULT NOW(),
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_reels_reel_id ON reels(reel_id);
CREATE INDEX IF NOT EXISTS idx_reels_creator_username ON reels(creator_username);
CREATE INDEX IF NOT EXISTS idx_reels_scraped_at ON reels(scraped_at);
CREATE INDEX IF NOT EXISTS idx_reels_likes ON reels(likes DESC);
CREATE INDEX IF NOT EXISTS idx_reels_views ON reels(views DESC);

-- Create a trigger to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_reels_updated_at BEFORE UPDATE ON reels
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Add Row Level Security (RLS) policies
ALTER TABLE reels ENABLE ROW LEVEL SECURITY;

-- Policy: Allow public read access (for viewing data)
CREATE POLICY "Allow public read access" ON reels
    FOR SELECT
    USING (true);

-- Policy: Allow authenticated inserts (for your service)
CREATE POLICY "Allow authenticated inserts" ON reels
    FOR INSERT
    WITH CHECK (true);

-- Policy: Allow authenticated updates
CREATE POLICY "Allow authenticated updates" ON reels
    FOR UPDATE
    USING (true)
    WITH CHECK (true);

-- Policy: Allow authenticated deletes
CREATE POLICY "Allow authenticated deletes" ON reels
    FOR DELETE
    USING (true);

-- Optional: Create a view for analytics
CREATE OR REPLACE VIEW reels_analytics AS
SELECT 
    creator_username,
    COUNT(*) as total_reels,
    AVG(likes) as avg_likes,
    AVG(views) as avg_views,
    MAX(likes) as max_likes,
    MAX(views) as max_views,
    jsonb_agg(DISTINCT category) as all_categories,
    DATE(scraped_at) as scrape_date
FROM reels
GROUP BY creator_username, DATE(scraped_at);

COMMENT ON TABLE reels IS 'Stores Instagram reels data with AI analysis';
COMMENT ON COLUMN reels.reel_id IS 'Unique Instagram reel identifier (shortcode)';
COMMENT ON COLUMN reels.reel_link IS 'Direct link to the reel video';
COMMENT ON COLUMN reels.caption IS 'Original caption text from the reel';
COMMENT ON COLUMN reels.creator_username IS 'Instagram username of the reel creator';
COMMENT ON COLUMN reels.creator_profile IS 'Profile URL of the creator';
COMMENT ON COLUMN reels.ai_summary IS 'AI-generated summary of the reel content';
COMMENT ON COLUMN reels.category IS 'JSON array of content categories';
COMMENT ON COLUMN reels.likes IS 'Number of likes on the reel';
COMMENT ON COLUMN reels.views IS 'Number of views on the reel';
COMMENT ON COLUMN reels.sentiment IS 'AI-analyzed sentiment of the content';
COMMENT ON COLUMN reels.top_comment_summary IS 'AI-generated summary of top comments';
COMMENT ON COLUMN reels.embeddings IS 'Vector embeddings for similarity search';
COMMENT ON COLUMN reels.top_comments IS 'JSON array of top comments';
COMMENT ON COLUMN reels.upload_date IS 'Date when reel was uploaded to Instagram';
COMMENT ON COLUMN reels.scraped_at IS 'Timestamp when data was scraped';
