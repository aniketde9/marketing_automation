## Marketing Automation Monorepo

This repository contains the **Next.js 14 frontend** and the **FastAPI worker** that power the Gemini-based marketing automation workflow.

### Structure

- `frontend/` – Next.js + Tailwind + shadcn/ui app deployed on Vercel. Handles Google OAuth, prompt management, Excel uploads, job creation, status polling, and download routes.
- `worker/` – Async FastAPI service deployed on Render. Polls NeonDB for pending jobs, decrypts user API keys, generates content with Gemini, and streams progress back to the database.
- `db/` – Placeholder for shared SQL schema & documentation (to be filled in during the DB/config phase).

### Prerequisites

- Node.js 18+ with npm (frontend)
- Python 3.11+ (worker)
- NeonDB Postgres connection
- Google Cloud project for OAuth + Gemini API keys

### Quick Start

```bash
# Frontend
cd frontend
npm install
npm run dev

# Worker
cd worker
python -m venv .venv && .venv\\Scripts\\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

### Testing

- **Frontend**: `npm run lint` (Next lint) and `npm run typecheck` (tsc) ensure the React app stays type-safe and style-compliant.
- **Worker**: `pytest` (once tests are added) plus ad-hoc `uvicorn main:app --reload` smoke tests. The FastAPI `/health` endpoint returns a `WorkerHealth` payload that CI can poll.

### Manual QA Checklist

1. Sign in with Google and verify the setup banner reflects the API key state.
2. Download the Excel template, fill 200 rows, and upload – confirm parsing success.
3. Start a generation job and observe the progress bar + log messages.
4. Download the result workbook after completion and ensure rows match.
5. Visit the Prompts tab, update a template, and reset to defaults.
6. Check the History tab for the last 15 days and delete an export.

### Next Steps

1. Populate `db/schema.sql` and environment samples (`frontend/.env.example`, `worker/.env.example`).
2. Configure local `.env` files (database URL, encryption key, OAuth secrets, worker URL).
3. Complete test suite + documentation updates (see project plan).

