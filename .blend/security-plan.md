# Security Plan: ChronoNoir Studio

> Generated 2026-02-28 | Phase 2 Architecture

## 1. Authentication Strategy

### Current State
- **chrono-canvas:** No user authentication. Single-user mode. `SECRET_KEY` env var exists but not wired to auth.
- **neo-mumbai-noir:** No authentication. Default user "default" in SQLite `users` table.

### MVP Target (Phase 0-2)
- **No auth required for hackathon MVP.** Single-user demo mode is sufficient for Devpost submission.
- Add `SECRET_KEY` validation on startup (chrono-canvas already has this guard).

### Post-MVP Target (Phase 3)
- Add session-based auth with email/password for B2C.
- Team Starter: invite-based workspace membership.
- Implementation: FastAPI + session cookies or JWT. PostgreSQL `users` table.

---

## 2. Secrets Management

### Consolidated .env Approach
Single `.env` file at project root, loaded by Docker Compose `env_file` directive.

| Secret | Required For | Current Location |
|--------|-------------|-----------------|
| `ANTHROPIC_API_KEY` | Claude LLM calls | chrono-canvas .env |
| `OPENAI_API_KEY` | GPT-4o LLM calls | chrono-canvas .env |
| `GOOGLE_API_KEY` | Gemini LLM calls | NEW |
| `SERPAPI_KEY` | Face reference search | chrono-canvas .env |
| `PEXELS_API_KEY` | Stock photo search | neo-mumbai-noir .env |
| `UNSPLASH_ACCESS_KEY` | Stock photo search | neo-mumbai-noir .env |
| `SECRET_KEY` | App security | chrono-canvas .env |
| `DATABASE_URL` | PostgreSQL connection | chrono-canvas .env |
| `REDIS_URL` | Redis connection | chrono-canvas .env |

### Actions
- Merge neo-mumbai-noir's `PEXELS_API_KEY` and `UNSPLASH_ACCESS_KEY` into consolidated `.env`
- Add `GOOGLE_API_KEY` for Gemini
- `.env` MUST be in `.gitignore` (already is in chrono-canvas)
- Provide `.env.example` with all keys listed but empty
- For GCP deployment: use Secret Manager for API keys

---

## 3. Network Isolation

### Docker Networks
| Network | Services | Exposed to Host? | Purpose |
|---------|----------|-------------------|---------|
| `frontend-net` | api, frontend | Yes (ports 3000, 8000) | User-facing |
| `db-net` | db, redis, api, worker | Yes (ports 5432, 6379 — dev only) | Data stores |
| `worker-net` | redis, api, worker | No | Job queue |
| `llm-net` | api, worker, noir-pipeline | No | LLM/host service access |

### Actions
- **Production:** Remove host port bindings for db (5432) and redis (6379) — internal only
- **noir-pipeline:** Only needs `llm-net` — no direct DB access, no frontend access
- Host services (Ollama, ComfyUI, FaceFusion) bind to `127.0.0.1` only, not `0.0.0.0`

---

## 4. Container Security (Existing)

chrono-canvas already implements:
- `security_opt: no-new-privileges:true` on all containers
- `cap_drop: ALL` on api, worker, frontend
- Non-root user in Dockerfiles (`appuser` uid 1000)
- `tmpfs: /tmp` to prevent persistent temp files

### Actions
- Apply same hardening to `noir-pipeline` container (currently runs as root)
- Add `read_only: true` filesystem where feasible

---

## 5. CORS and API Routing

### Current
- `CORS_ORIGINS=["http://localhost:3000"]` — restricts to frontend origin only
- API serves on `/api/*` prefix — clean namespace

### Actions
- For GCP deployment: update `CORS_ORIGINS` to include deployed frontend URL
- Add rate limiting middleware to API (RATE_LIMIT_RPM=60 already configured)
- Consider Nginx reverse proxy in front of API for production (frontend container already uses Nginx)

---

## 6. Upload/Input Security

### Current (chrono-canvas)
- Face upload: JPEG/PNG/WebP only, 10MB max, **magic bytes validation** (not just MIME type)
- Content moderation: keyword-based filtering on input text and research output
- SSRF protection: exists but has known DNS rebinding vulnerability (bead `history-faces-7g4`)

### Actions
- Fix SSRF DNS rebinding vulnerability (existing P2 bug)
- Apply same magic-bytes validation to any file uploads in storyboard pipeline
- Validate image dimensions (max resolution) to prevent resource exhaustion
- Sanitize story text input (strip HTML, limit length)

---

## 7. Third-Party Service Security

| Service | Risk | Mitigation |
|---------|------|------------|
| Ollama | Local only, no auth | Bind to 127.0.0.1 only |
| ComfyUI | Local only, no auth | Bind to 127.0.0.1 only |
| FaceFusion | Local only, no auth | Bind to 127.0.0.1 only |
| Pexels/Unsplash | API key in requests | Keys in .env, not logged |
| Claude/OpenAI/Gemini | API keys in requests | Keys in .env, not logged, cost tracking active |
| SerpAPI | API key in requests | Key in .env, gated by FACE_SEARCH_ENABLED toggle |

### Actions
- Ensure no API keys appear in audit_logs or agent_trace JSONB columns
- Add cost ceiling alerts (daily/weekly max spend per LLM provider)
- Log LLM costs but redact prompt content in production logs

---

## 8. Data Protection

| Data | Storage | Retention | Access |
|------|---------|-----------|--------|
| User stories/prompts | PostgreSQL | 30 days (NFR5) | API only |
| Generated images | output/ volume | Until cleanup | API + export |
| Face uploads | uploads/ volume | Until cleanup | API only |
| Audit trail | PostgreSQL audit_logs | 30 days minimum | Admin API |
| Research cache | PostgreSQL + pgvector | Indefinite (cost savings) | Internal |

### Actions
- Add TTL cleanup job for output/ and uploads/ older than 30 days
- Ensure face uploads are not included in public export bundles without consent
- Add `X-Content-Type-Options: nosniff` header on all API responses
