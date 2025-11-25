import { neon } from '@neondatabase/serverless';

if (!process.env.DATABASE_URL) {
  throw new Error('DATABASE_URL is not set');
}

export const sql = neon(process.env.DATABASE_URL);

export type User = {
  id: string;
  email: string;
  google_id: string;
  name: string | null;
  gemini_api_key_encrypted: string | null;
  created_at: Date;
  updated_at: Date;
};

export type JobStatus = 'pending' | 'processing' | 'completed' | 'failed';

export type Job = {
  id: string;
  user_id: string;
  status: JobStatus;
  progress: number;
  total: number;
  latest_message: string | null;
  error_message: string | null;
  started_at: Date | null;
  completed_at: Date | null;
  created_at: Date;
};

export type PromptTemplates = {
  carousel?: string;
  short_linkedin?: string;
  short_x?: string;
  short_instagram?: string;
  thread_x?: string;
  mixed?: string;
  short_posts?: string;
};

export type Prompt = {
  user_id: string;
  templates: PromptTemplates;
  updated_at: Date;
};

