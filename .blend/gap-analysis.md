# Gap Analysis: ChronoNoir Studio MVP

> Generated 2026-02-28 | Phase 1 Discovery

## Verdict Legend
- **EXISTS** — directly available in an input project, usable as-is
- **PARTIAL** — baseline exists but needs modification for the blended product
- **GAP** — not present in any input project, must be built
- **CONFLICT** — both projects provide it but incompatibly

---

## Phase -1: Devpost Compliance

| ID | Requirement | chrono-canvas | neo-mumbai-noir | Verdict | Notes |
|----|------------|---------------|-----------------|---------|-------|
| RD.1 | Gemini model for narrative/planning | GAP — uses Claude/OpenAI/Ollama | GAP — uses Ollama only | **GAP** | Must add Gemini provider to LLM router |
| RD.2 | Google GenAI SDK or ADK | GAP — uses Anthropic/OpenAI SDKs | GAP — uses raw HTTP to Ollama | **GAP** | Must implement GenAI SDK/ADK orchestration path |
| RD.3 | GCP deployment + GCP storage | PARTIAL — GKE manifests exist (`deploy/gke/`) but no blended proof flow | GAP | **PARTIAL** | GKE scaffolding exists; need Cloud Run/GKE deployment + GCP storage for artifacts |
| RD.4 | Multimodal I/O (text+image+audio+video) | PARTIAL — text+image exists, no audio/video | PARTIAL — text+image exists, no audio/video | **GAP** | Audio narration and video stitch are new capabilities |
| RD.5 | Interleaved mixed output stream | PARTIAL — WebSocket streams text progress + final image | GAP | **PARTIAL** | WebSocket exists; need interleaved media milestones |
| RS.1 | Public repo with reproducible spin-up | PARTIAL — Makefile + docker-compose exist | PARTIAL — start.sh exists | **PARTIAL** | Need unified judge-ready README |
| RS.2 | GCP deployment proof | GAP | GAP | **GAP** | No recording/evidence workflow |
| RS.3 | Architecture diagram | GAP | GAP | **GAP** | Mermaid diagrams needed |
| RS.4 | <4 min demo video | GAP | GAP | **GAP** | Demo runbook + recording needed |

---

## Phase 0: Unified Entry + Onboarding

| ID | Requirement | chrono-canvas | neo-mumbai-noir | Verdict | Notes |
|----|------------|---------------|-----------------|---------|-------|
| R0.1 | Mode selection in <=2 clicks | PARTIAL — has route-based nav (`App.tsx`) but no mode selector | PARTIAL — has tab-based UI (`unified_ui.py`) with 7 tabs | **PARTIAL** | Need unified mode switch: Story Director vs Historical Lens in React frontend |
| R0.2 | One prebuilt template per mode | GAP | GAP | **GAP** | No template/preset system in either project |
| R0.3 | Empty-state guidance | GAP — Generate page has form but no guidance | PARTIAL — Guide tab loads PRD.md | **GAP** | Need onboarding copy with time-to-result messaging |

---

## Phase 1: Core Generation Workflows

| ID | Requirement | chrono-canvas | neo-mumbai-noir | Verdict | Notes |
|----|------------|---------------|-----------------|---------|-------|
| R1.1 | Free-text prompt → image output | EXISTS — `POST /api/generate` with full pipeline | EXISTS — Story tab → extraction → generation | **EXISTS** | Both have this; chrono-canvas is API-backed with persistent records |
| R1.2 | Storyboard: >=3 scene outputs per run | GAP — portrait-centric (1 output per run) | EXISTS — Storyboard tab assembles multi-scene output from characters + images | **PARTIAL** | Neo has the workflow but not as API-backed durable run artifacts in chrono-canvas model |
| R1.3 | Portrait: 1 primary output per run | EXISTS — core pipeline produces 1 portrait per generation request | N/A | **EXISTS** | Directly available |
| R1.4 | Export on completed outputs | EXISTS — `GET /api/export/{id}/download` + Export.tsx page | PARTIAL — Gallery tab shows images but no structured export | **EXISTS** | chrono-canvas has full export path |
| FR1 | Both pipelines from one account | PARTIAL — only portrait pipeline exists | N/A | **PARTIAL** | Need to add `creative_story` run type |
| FR2 | Persistent run records | EXISTS — generation_requests table with full trace | PARTIAL — SQLite stores stories/characters but not as "run" records | **EXISTS** | chrono-canvas model is the target |
| FR3 | Revisit prior outputs + re-export | EXISTS — AuditList.tsx, AuditDetail.tsx pages | PARTIAL — Gallery tab shows past images | **EXISTS** | chrono-canvas has audit trail UI |
| FR4 | Output cards: mode, time, export state | PARTIAL — shows status but not mode (single-mode currently) | GAP | **PARTIAL** | Need to add mode field to output cards |

---

## Phase 2: Trust Layer + Personalization

| ID | Requirement | chrono-canvas | neo-mumbai-noir | Verdict | Notes |
|----|------------|---------------|-----------------|---------|-------|
| R2.1 | Validation summary on outputs | EXISTS — `GET /api/validation/{id}`, ValidationSummary model, AuditDetail page | GAP | **EXISTS** | Validation pipeline with 0-100 scoring exists |
| R2.2 | Provenance summary per output | EXISTS — audit_logs table tracks prompts, tokens, costs, latency per LLM call | GAP | **PARTIAL** | Audit exists but not as concise export-ready trust card |
| R2.3 | Face upload + attach to request | EXISTS — `POST /api/faces/upload` (JPEG/PNG/WebP, 10MB, magic bytes) | PARTIAL — FaceFusion tab takes source face path | **EXISTS** | chrono-canvas has validated upload endpoint |
| R2.4 | Original + personalized output (or fallback) | PARTIAL — FaceFusion compositing node exists but no dual-output presentation | PARTIAL — FaceFusion swap produces output but no original comparison | **PARTIAL** | Need dual-output response contract |
| R2.5 | Compare view (original vs personalized) | GAP — no side-by-side compare component | GAP | **GAP** | New UI component needed |
| FR5 | Safety notice before face personalization | GAP | GAP | **GAP** | Consent UX needed |

---

## Phase 3: Monetization + Team Starter

| ID | Requirement | chrono-canvas | neo-mumbai-noir | Verdict | Notes |
|----|------------|---------------|-----------------|---------|-------|
| R3.1 | Credit usage visible in UI | GAP | GAP | **GAP** | No credit/metering system |
| R3.2 | Free plan: monthly cap + watermark | GAP | GAP | **GAP** | No plan gating |
| R3.3 | Plus plan: no watermark + more credits | GAP | GAP | **GAP** | No billing integration |
| R3.4 | Team Starter: shared project (10 seats) | GAP — no multi-user | PARTIAL — users table exists in SQLite | **GAP** | No workspace/team model |
| R3.5 | Review statuses: Draft/In Review/Approved | PARTIAL — human_review_status on generation_requests (accept/reject/flag) | GAP | **PARTIAL** | Exists but needs Draft/In Review/Approved states |

---

## Non-Functional Requirements

| ID | Requirement | chrono-canvas | neo-mumbai-noir | Verdict | Notes |
|----|------------|---------------|-----------------|---------|-------|
| NFR1 | 99.0% weekly uptime | PARTIAL — Docker + GKE scaffolding, health checks exist | GAP — single container, no HA | **PARTIAL** | GKE path exists but not production-hardened |
| NFR2 | Status updates visible within 3s | EXISTS — WebSocket streaming via Redis pub/sub | GAP — no async progress | **EXISTS** | chrono-canvas has real-time progress |
| NFR3 | 50 concurrent sessions | PARTIAL — ARQ worker (max 5 concurrent), HPA in GKE | GAP — single-threaded Gradio | **PARTIAL** | Need to tune worker concurrency + HPA |
| NFR4 | Actionable error messages | PARTIAL — errors exist but vary in quality | GAP | **PARTIAL** | Error message audit needed |
| NFR5 | Audit records retained 30 days | EXISTS — PostgreSQL audit_logs with no TTL | N/A | **EXISTS** | Add TTL policy if needed |

---

## UX Requirements

| ID | Requirement | chrono-canvas | neo-mumbai-noir | Verdict | Notes |
|----|------------|---------------|-----------------|---------|-------|
| UX1 | Quick start + advanced paths | GAP | GAP | **GAP** | New onboarding flow |
| UX2 | Plain-language progress labels | PARTIAL — StreamingText component exists | GAP | **PARTIAL** | Labels need UX review |
| UX3 | Result page CTA: Export | EXISTS — Export.tsx page | GAP | **EXISTS** | Export page exists |
| UX4 | Compare view on desktop + mobile | GAP | GAP | **GAP** | Responsive compare component needed |

---

## Analytics & Instrumentation

| ID | Requirement | chrono-canvas | neo-mumbai-noir | Verdict | Notes |
|----|------------|---------------|-----------------|---------|-------|
| Events | 9 required events | GAP — no client analytics | GAP | **GAP** | No analytics SDK integrated |
| Properties | user_id, run_id, mode, etc. | PARTIAL — run_id exists, no user_id/mode/plan_type tracking | GAP | **GAP** | Need analytics instrumentation |

---

## Devpost Cross-Cutting (from Phase Module Map)

| Requirement | chrono-canvas | neo-mumbai-noir | Verdict |
|------------|---------------|-----------------|---------|
| Must use Gemini | GAP | GAP | **GAP** |
| Must use GenAI SDK/ADK | GAP | GAP | **GAP** |
| Must use Google Cloud service | PARTIAL (GKE scaffolding) | GAP | **PARTIAL** |
| Multimodal beyond text-only | PARTIAL (text+image) | PARTIAL (text+image) | **PARTIAL** — need audio+video |
| Demo/proof artifacts | GAP | GAP | **GAP** |

---

## Summary Counts

| Verdict | Phase -1 | Phase 0 | Phase 1 | Phase 2 | Phase 3 | NFR | UX | Analytics | Total |
|---------|----------|---------|---------|---------|---------|-----|-----|-----------|-------|
| EXISTS | 0 | 0 | 4 | 2 | 0 | 2 | 1 | 0 | **9** |
| PARTIAL | 2 | 1 | 2 | 2 | 1 | 3 | 1 | 0 | **12** |
| GAP | 7 | 2 | 0 | 2 | 4 | 0 | 2 | 2 | **19** |
| CONFLICT | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | **0** |

**Key Takeaway:** 19 gaps + 12 partial items to close. The biggest gap clusters are:
1. **Devpost compliance** (Gemini, GenAI SDK, GCP proof, demo artifacts) — 7 gaps
2. **Monetization/Team** (credits, billing, workspaces) — 4 gaps
3. **Multimodal output** (audio narration, video stitch, interleaved streaming) — contained in Phase -1/2
4. **Storyboard integration** — Neo's workflow needs to become API-backed run artifacts in chrono-canvas
