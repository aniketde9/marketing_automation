<!-- 89c9e227-6f62-4a7d-a0d7-3de58b674a54 de374f95-ebd6-4a02-98f7-0fd78691befc -->
# Marketing Automation Revamp Plan

## Phase 1 – Repository Preparation

1. Verify current Python worker structure (`main.py`, `utils.py`, `prompts/`) and identify reusable logic.
2. Create `frontend/` and `worker/` folders if missing; move existing Python files under `worker/` while keeping git history intact.
3. Add a root `README.md` outline describing the new multi-app setup plus prerequisites (Node, Python, NeonDB).

## Phase 2 – Frontend (Next.js) Implementation

1. Scaffold Next.js 14 App Router project in `frontend/` with Tailwind + shadcn/ui (per instructions) and configure `package.json`, `tsconfig.json`, `.eslintrc`.
2. Implement shared utilities under `frontend/lib/`:

- `db.ts` using `@neondatabase/serverless` with typed helpers for `users`, `jobs`, `prompts`.
- `auth.ts` for NextAuth Google provider + session augmentation.
- `encryption.ts` and `excel.ts` per provided specs.

3. Build API routes (`app/api/*`) for auth, prompts, setup-key, upload-excel, create-job, job-status, download-result, download-template, history. Ensure routes call utilities, handle errors, and enforce auth.
4. Create UI pages under `app/(auth)` and `app/(dashboard)` (login, setup API key, prompts, generate, history) wiring shadcn components, form handling, polling, and toast feedback.
5. Add shared UI components (`components/ui`, `components/auth`, `components/prompts`, `components/generate`) and global layout with NextAuth session provider and protected routes.

## Phase 3 – Python Worker Enhancements

1. Restructure existing FastAPI code into `worker/` with modules (`main.py`, `db.py`, `gemini_generator.py`, `prompts.py`, `models.py`).
2. Implement AES-256-CBC decryption in `db.py` matching frontend encryption, switch to asyncpg pooled operations, and extend helper methods for jobs/files/logs.
3. Update `main.py` job processor loop for robust status updates, per-topic progress, retries, and logging; ensure graceful shutdown and health endpoint.
4. Expand `gemini_generator.py` with explicit rate-limit enforcement, exponential backoff, and error surface to DB.
5. Add FastAPI Pydantic schemas (`models.py`) plus configuration loading from `.env`; ensure `requirements.txt` lists pinned versions; add optional `Dockerfile` or `render.yaml` for Render deployment.

## Phase 4 – Database & Config

1. Add `db/schema.sql` with provided tables, indexes, and housekeeping function; include instructions for running on NeonDB.
2. Document `.env.local` (frontend) and `.env` (worker) variables; add `.env.example` files for both apps referencing encryption key, DB URL, OAuth, worker URL.
3. Provide scripts or npm/pip commands for local dev (`frontend/package.json` scripts, `worker/Makefile` or `README` section).

## Phase 5 – Testing & Validation

1. Implement unit/integration tests where feasible (e.g., encryption utility, Excel parser, FastAPI endpoint smoke tests) and add to scripts (`npm test`, `pytest`).
2. Create manual QA checklist covering OAuth login, API-key setup, template download/upload, job creation, worker processing, history cleanup.
3. Verify ESLint/Tailwind checks and formatters (Prettier) run cleanly; add Husky hook if desired.

## Phase 6 – Deployment Prep

1. Add `vercel.json` (if needed) and deployment instructions for Next.js (env vars, build command) plus `render.yaml` for worker service.
2. Describe NeonDB provisioning, schema migration, and encryption key generation steps in README.
3. Provide cron-job instructions for keeping the Render worker awake.

## Phase 7 – Project Documentation

1. Update root `README.md` with architecture diagram, feature list, local setup steps, env configuration, and deployment workflow.
2. Add `docs/` folder (optional) for API reference, Excel template guide, and troubleshooting tips.

### To-dos

- [ ] Create frontend/ & worker/ scaffolds
- [ ] Implement Next.js lib & API routes
- [ ] Build auth/dashboard pages & components
- [ ] Refactor FastAPI worker modules
- [ ] Add schema.sql and env samples
- [ ] Add tests, README, deployment notes