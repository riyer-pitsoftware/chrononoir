# Scaling Plan: ChronoNoir Studio

> Generated 2026-02-28 | Phase 2 Architecture

## 1. Bottleneck Analysis

| Service | Latency | Bottleneck Type | Notes |
|---------|---------|-----------------|-------|
| **ComfyUI image generation** | 30-120s per image | **GPU-bound, singleton** | Longest single step. SDXL/FLUX generation is serial per GPU. |
| **FaceFusion face swap** | 10-30s per image | **GPU-bound, singleton** | Face swapping uses GPU. Serial per request. |
| **LLM calls (Gemini/Claude)** | 2-10s per call | **Network + rate-limited** | Multiple calls per run (extraction, research, prompt, validation). |
| **Ollama** | 1-5s per call | **CPU/GPU-bound** | Local inference. Faster but lower quality. |
| PostgreSQL | <50ms | Not a bottleneck | Async driver, connection pooling via SQLAlchemy. |
| Redis | <10ms | Not a bottleneck | In-memory. Pub/sub + job queue. |

### Critical Path Timing (Creative Storyteller run)
```
Orchestration (Ollama):     ~2s
Extraction (Gemini):        ~5s
Research (Gemini):           ~5s
Prompt Gen x3 (Gemini):     ~9s  (3 scenes)
Image Gen x3 (ComfyUI):    ~180s (3 scenes @ ~60s each — SERIAL)
Validation (Gemini):         ~5s
Face Swap x3 (FaceFusion):  ~60s (3 scenes @ ~20s each — SERIAL)
─────────────────────────────────
Total estimate:             ~266s (~4.4 minutes)
```

**ComfyUI is the dominant bottleneck** — 68% of total run time.

---

## 2. Concurrency Target

**NFR3:** 50 concurrent active generation sessions in beta.

### Current Capacity
- ARQ worker: max 5 concurrent jobs (configurable)
- ComfyUI: 1 concurrent generation (GPU-bound, queue-based)
- FaceFusion: 1 concurrent swap (GPU-bound)

### Gap
50 concurrent sessions with serial GPU access = massive queue backlog. At ~4.4 min per creative story run, 50 concurrent means:
- Queue wait time: up to 50 * 4.4 = 220 minutes for last-in-queue
- Unacceptable for MVP

### Mitigation Strategy (Phases)

**Phase 1 (MVP):** Target 5-10 concurrent sessions realistically
- ARQ workers: 5 concurrent
- ComfyUI: 1 instance (single GPU)
- Accept longer queue times, communicate wait via WebSocket progress
- Optimize: batch LLM calls where possible, reduce image steps per scene

**Phase 2 (Beta):** Target 20-30 concurrent
- Multiple ComfyUI workers (if multi-GPU available)
- Queue-based decoupling (see below)
- Faster models (FLUX schnell for draft quality)

**Phase 3 (Scale):** Target 50+ concurrent
- Cloud GPU instances (GCP GPU VMs or Cloud Run GPU)
- Horizontal scaling of worker pods (GKE HPA already scaffolded)

---

## 3. Horizontal Scaling Candidates

| Service | Scalable? | Strategy |
|---------|-----------|----------|
| `api` | Yes | Stateless FastAPI. Add replicas behind load balancer. |
| `worker` | Yes | ARQ workers are independent. Add replicas to increase parallelism. |
| `frontend` | Yes | Static assets served by Nginx. CDN-ready. |
| `db` | Vertical only (MVP) | Single PostgreSQL. Read replicas for scale. |
| `redis` | Vertical only (MVP) | Single Redis. Cluster for scale. |
| ComfyUI | **Limited** | GPU-bound singleton per GPU. Multi-GPU = multi-instance. |
| FaceFusion | **Limited** | GPU-bound singleton per GPU. |
| Ollama | Moderate | CPU-capable but slow. GPU-accelerated. Can run multiple model instances. |

---

## 4. Queue-Based Decoupling Opportunities

### Current
API → Redis (ARQ) → Worker → LangGraph (synchronous pipeline within worker)

### Recommended
Break the monolithic pipeline into queued stages:

```
Stage 1: Extraction + Research (LLM-heavy, parallel-safe)
  ↓ Redis queue
Stage 2: Image Generation (GPU-heavy, serial per GPU)
  ↓ Redis queue
Stage 3: Validation + Compositing (LLM + GPU)
  ↓ Redis queue
Stage 4: Export + Notification
```

**Benefit:** Stage 1 can process many requests in parallel (LLM calls). Stage 2 queues fairly for GPU access. Stages don't block each other.

**Implementation:** Extend ARQ with multiple task types. LangGraph already supports checkpointing between nodes (PostgreSQL checkpointer is active).

---

## 5. Resource Estimates

| Service | CPU | Memory | GPU VRAM | Disk |
|---------|-----|--------|----------|------|
| PostgreSQL | 1 core | 512MB-1GB | — | 10GB+ (grows with runs) |
| Redis | 0.5 core | 256MB | — | — |
| API | 1 core | 512MB | — | — |
| Worker | 2 cores | 1-2GB | — | — |
| Frontend | 0.5 core | 256MB | — | 100MB |
| Noir Pipeline | 1 core | 512MB | — | 1GB (images) |
| **Ollama** | 2-4 cores | 4-8GB | 4GB (optional) | 5GB (models) |
| **ComfyUI** | 2 cores | 4-8GB | **8GB+ (required)** | 10GB+ (models + outputs) |
| **FaceFusion** | 2 cores | 2-4GB | **4-8GB (required)** | 2GB (models) |

### Minimum Machine Spec (Dev/Demo)
- **CPU:** 8 cores
- **RAM:** 16GB
- **GPU:** 1x with 10GB+ VRAM (RTX 3060 or better / M1 Pro+)
- **Disk:** 50GB SSD

### Recommended Machine Spec (Beta)
- **CPU:** 16 cores
- **RAM:** 32GB
- **GPU:** 1x 24GB VRAM (RTX 4090) or 2x 12GB
- **Disk:** 100GB SSD

---

## 6. Performance Quick Wins

| Optimization | Impact | Effort |
|-------------|--------|--------|
| Use FLUX schnell (4-step) for draft previews | 3-5x faster image gen | Low |
| Cache research results (already implemented via pgvector) | Skip LLM calls for known figures | Done |
| Batch LLM calls where independent (e.g., 3 scene prompts) | 3x faster prompt gen | Medium |
| Progressive image delivery via WebSocket | Better perceived performance | Medium |
| Pre-warm ComfyUI with first prompt on startup | Eliminates cold start penalty | Low |
