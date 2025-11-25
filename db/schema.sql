-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Users table
CREATE TABLE IF NOT EXISTS users (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  email VARCHAR(255) UNIQUE NOT NULL,
  google_id VARCHAR(255) UNIQUE NOT NULL,
  name VARCHAR(255),
  gemini_api_key_encrypted TEXT,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

-- Custom prompts
CREATE TABLE IF NOT EXISTS prompts (
  user_id UUID PRIMARY KEY REFERENCES users(id) ON DELETE CASCADE,
  templates JSONB NOT NULL DEFAULT '{}'::jsonb,
  updated_at TIMESTAMP DEFAULT NOW()
);

-- Generation jobs
CREATE TABLE IF NOT EXISTS jobs (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID REFERENCES users(id) ON DELETE CASCADE,
  status VARCHAR(20) DEFAULT 'pending',
  progress INT DEFAULT 0,
  total INT DEFAULT 200,
  latest_message TEXT,
  error_message TEXT,
  started_at TIMESTAMP,
  completed_at TIMESTAMP,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

-- Generated content rows
CREATE TABLE IF NOT EXISTS generated_content (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  job_id UUID REFERENCES jobs(id) ON DELETE CASCADE,
  row_number INT NOT NULL,
  content_type VARCHAR(50),
  topic TEXT,
  generated_text TEXT,
  created_at TIMESTAMP DEFAULT NOW()
);

-- Files
CREATE TABLE IF NOT EXISTS files (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  job_id UUID REFERENCES jobs(id) ON DELETE CASCADE,
  user_id UUID REFERENCES users(id) ON DELETE CASCADE,
  file_name VARCHAR(255),
  file_data BYTEA,
  file_size INT,
  created_at TIMESTAMP DEFAULT NOW()
);

-- User generation tracking
CREATE TABLE IF NOT EXISTS user_generation_log (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID REFERENCES users(id) ON DELETE CASCADE,
  job_id UUID REFERENCES jobs(id),
  generation_date DATE NOT NULL,
  posts_generated INT DEFAULT 0,
  created_at TIMESTAMP DEFAULT NOW(),
  UNIQUE (user_id, generation_date)
);

-- Helpful indexes
CREATE INDEX IF NOT EXISTS idx_jobs_user_status ON jobs(user_id, status);
CREATE INDEX IF NOT EXISTS idx_jobs_status ON jobs(status);
CREATE INDEX IF NOT EXISTS idx_files_user_created ON files(user_id, created_at);
CREATE INDEX IF NOT EXISTS idx_user_gen_log_user_date ON user_generation_log(user_id, generation_date);

-- Cleanup helper
CREATE OR REPLACE FUNCTION delete_old_files()
RETURNS void AS $$
BEGIN
  DELETE FROM files WHERE created_at < NOW() - INTERVAL '15 days';
END;
$$ LANGUAGE plpgsql;

