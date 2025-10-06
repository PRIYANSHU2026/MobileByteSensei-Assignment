-- Supabase Database Schema for Instagram Reels Analyzer
-- Run this SQL in your Supabase SQL Editor to create the necessary tables

-- Create reels table
CREATE TABLE IF NOT EXISTS instagram_reels (
    id BIGSERIAL PRIMARY KEY,
    reel_id TEXT UNIQUE NOT NULL,
    reel_link TEXT,
    caption TEXT,
    creator_username TEXT,
    creator_profile TEXT,
    ai_summary TEXT,
    category TEXT[], -- Array of categories
    likes INTEGER DEFAULT 0,
    views INTEGER DEFAULT 0,
    sentiment TEXT,
    top_comment_summary TEXT,
    embeddings FLOAT8[], -- Array of floats for embeddings
    upload_date TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Create comments table
CREATE TABLE IF NOT EXISTS reel_comments (
    id BIGSERIAL PRIMARY KEY,
    reel_id TEXT NOT NULL,
    user_name TEXT,
    comment_text TEXT,
    comment_timestamp TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    FOREIGN KEY (reel_id) REFERENCES instagram_reels(reel_id) ON DELETE CASCADE
);

-- Create index for faster queries
CREATE INDEX IF NOT EXISTS idx_reels_reel_id ON instagram_reels(reel_id);
CREATE INDEX IF NOT EXISTS idx_reels_creator ON instagram_reels(creator_username);
CREATE INDEX IF NOT EXISTS idx_reels_sentiment ON instagram_reels(sentiment);
CREATE INDEX IF NOT EXISTS idx_reels_created_at ON instagram_reels(created_at);
CREATE INDEX IF NOT EXISTS idx_comments_reel_id ON reel_comments(reel_id);

-- Create updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_instagram_reels_updated_at
    BEFORE UPDATE ON instagram_reels
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Enable Row Level Security (RLS)
ALTER TABLE instagram_reels ENABLE ROW LEVEL SECURITY;
ALTER TABLE reel_comments ENABLE ROW LEVEL SECURITY;

-- Create policies for public read access (adjust based on your needs)
CREATE POLICY "Allow public read access" ON instagram_reels
    FOR SELECT USING (true);

CREATE POLICY "Allow public insert access" ON instagram_reels
    FOR INSERT WITH CHECK (true);

CREATE POLICY "Allow public read access" ON reel_comments
    FOR SELECT USING (true);

CREATE POLICY "Allow public insert access" ON reel_comments
    FOR INSERT WITH CHECK (true);

-- Optional: Create a view for easy querying
CREATE OR REPLACE VIEW reels_with_comments AS
SELECT 
    r.*,
    COALESCE(
        json_agg(
            json_build_object(
                'user', c.user_name,
                'comment', c.comment_text,
                'timestamp', c.comment_timestamp
            ) ORDER BY c.created_at
        ) FILTER (WHERE c.id IS NOT NULL),
        '[]'::json
    ) as comments
FROM instagram_reels r
LEFT JOIN reel_comments c ON r.reel_id = c.reel_id
GROUP BY r.id;
