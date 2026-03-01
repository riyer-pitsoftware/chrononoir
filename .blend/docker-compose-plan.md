# Docker Compose Plan: ChronoNoir Studio

> Generated 2026-02-28 | Phase 2 Architecture

## Unified Service Inventory

| Service | Source | Image/Build | Port | Type | Network | Depends On |
|---------|--------|-------------|------|------|---------|------------|
| `db` | chrono-canvas | pgvector/pgvector:pg16 | 5432 | container | db-net | — |
| `redis` | chrono-canvas | redis:7-alpine | 6379 | container | db-net, worker-net | — |
| `api` | chrono-canvas | Dockerfile.api (Python 3.11) | 8000 | container | frontend-net, db-net, worker-net, llm-net | db (healthy), redis (healthy) |
| `worker` | chrono-canvas | Dockerfile.api (ARQ) | — | container | db-net, worker-net, llm-net | db (healthy), redis (healthy) |
| `frontend` | chrono-canvas | Dockerfile.frontend (Nginx/Node) | 3000 | container | frontend-net | api |
| `noir-pipeline` | neo-mumbai-noir | Dockerfile (Python 3.11) | 7860 | container | llm-net | — |
| Ollama | host | — | 11434 | host process | host.docker.internal | GPU optional |
| ComfyUI | host | — | 8188 | host process | host.docker.internal | GPU required |
| FaceFusion | host | — | 7870 | host process | host.docker.internal | GPU required |

### Service Strategy Notes

**Kept from chrono-canvas as-is:**
- `db`, `redis`, `api`, `worker`, `frontend` — production-proven, security-hardened (no-new-privileges, cap_drop ALL)

**Kept from neo-mumbai-noir as-is:**
- `noir-pipeline` — Gradio UI remains available for standalone creative workflow; also serves as the Neo module host that chrono-canvas API calls into

**GPU services on host (not containerized):**
- **Ollama** (port 11434): Both projects use it. Single instance, multiple models coexist (llama3.1:8b, llama3.2). Containers reach via `host.docker.internal:11434`
- **ComfyUI** (port 8188): Both projects use identical HTTP+WebSocket API. Single instance. Containers reach via `host.docker.internal:8188`
- **FaceFusion** (port 7870): Standardize on Neo's `facefusion_server.py` HTTP wrapper on port 7870. chrono-canvas `FACEFUSION_API_URL` repoints to 7870. Containers reach via `host.docker.internal:7870`

**Retired:**
- chrono-canvas Docker FaceFusion service (port 7861) — replaced by host-based FaceFusion at 7870 for GPU access

---

## Network Topology

| Network | Services | Purpose |
|---------|----------|---------|
| `frontend-net` | api, frontend | Frontend ↔ API communication |
| `db-net` | db, redis, api, worker | Database + cache access |
| `worker-net` | redis, api, worker | Job queue communication |
| `llm-net` | api, worker, noir-pipeline | LLM and host service access |

All GPU services run on host. Containers reach them via `extra_hosts: host.docker.internal:host-gateway`.

---

## Volume Strategy

| Volume | Mount | Purpose | Shared By |
|--------|-------|---------|-----------|
| `pgdata` | /var/lib/postgresql/data | PostgreSQL persistent data | db |
| `output` | /app/output | Generated images, exports | api, worker, noir-pipeline |
| `uploads` | /app/uploads | User face uploads | api, worker |
| `noir-data` | /app/data | Neo SQLite DB (transitional) | noir-pipeline |

**Key:** `output` volume is shared between api/worker and noir-pipeline so generated images from either pipeline are accessible for export.

---

## Startup Ordering

```
1. db         (healthcheck: pg_isready)
2. redis      (healthcheck: redis-cli ping)
3. api        (depends_on: db healthy, redis healthy; runs migrations)
4. worker     (depends_on: db healthy, redis healthy)
5. frontend   (depends_on: api)
6. noir-pipeline (independent, but needs host services)
```

**Host services (started before `docker compose up`):**
```
1. Ollama     (port 11434)
2. ComfyUI    (port 8188)
3. FaceFusion (port 7870)
```

Use Neo's `start.sh` pattern: check each host service is reachable before starting Docker stack.

---

## Consolidated Environment Variables

```env
# ── Database ──
DATABASE_URL=postgresql+asyncpg://chronocanvas:chronocanvas@db:5432/chronocanvas
REDIS_URL=redis://redis:6379/0

# ── LLM Providers (standardized names) ──
OLLAMA_BASE_URL=http://host.docker.internal:11434
ANTHROPIC_API_KEY=
OPENAI_API_KEY=
GOOGLE_API_KEY=                    # NEW: Gemini
SERPAPI_KEY=

# ── LLM Routing ──
DEFAULT_LLM_PROVIDER=ollama
OLLAMA_MODEL=llama3.1:8b
CLAUDE_MODEL=claude-sonnet-4-5-20250929
OPENAI_MODEL=gpt-4o
GEMINI_MODEL=gemini-2.5-pro        # NEW

# ── Image Generation (standardized) ──
IMAGE_PROVIDER=comfyui
COMFYUI_API_URL=http://host.docker.internal:8188
COMFYUI_MODEL=sdxl
COMFYUI_SDXL_CHECKPOINT=juggernautXL_v9.safetensors

# ── FaceFusion (standardized to host server) ──
FACEFUSION_API_URL=http://host.docker.internal:7870
FACEFUSION_ENABLED=true

# ── Stock Image Search (from neo-mumbai-noir) ──
PEXELS_API_KEY=
UNSPLASH_ACCESS_KEY=

# ── Security ──
SECRET_KEY=change-me-in-production
CONTENT_MODERATION_ENABLED=true

# ── Storage ──
UPLOAD_DIR=./uploads
OUTPUT_DIR=./output

# ── API ──
API_HOST=0.0.0.0
API_PORT=8000
CORS_ORIGINS=["http://localhost:3000"]

# ── Pipeline ──
VALIDATION_RETRY_ENABLED=true
FACE_SEARCH_ENABLED=true
RESEARCH_CACHE_ENABLED=true
```

### Env Var Resolutions
| Conflict | Resolution |
|----------|-----------|
| `OLLAMA_HOST` vs `OLLAMA_BASE_URL` | Standardize to `OLLAMA_BASE_URL` (chrono-canvas convention). Neo code updated to read this. |
| `COMFYUI_HOST` vs `COMFYUI_API_URL` | Standardize to `COMFYUI_API_URL`. Neo code updated. |
| `FACEFUSION_HOST` vs `FACEFUSION_API_URL` | Standardize to `FACEFUSION_API_URL` at port 7870. |
