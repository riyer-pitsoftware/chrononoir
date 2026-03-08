# Gap Analysis: ChronoNoir Studio MVP

> Generated 2026-02-28 | Updated 2026-03-08

## Verdict Legend
- **EXISTS** — directly available in an input project, usable as-is
- **PARTIAL** — baseline exists but needs modification for the blended product
- **GAP** — not present in any input project, must be built
- **CONFLICT** — both projects provide it but incompatibly

---

## Phase -1: Devpost Compliance

| ID | Requirement | chrono-canvas | neo-mumbai-noir | Verdict | Notes |
|----|------------|---------------|-----------------|---------|-------|
| RD.1 | Gemini model for narrative/planning | EXISTS — Gemini provider in LLM router | GAP — uses Ollama only | **EXISTS** | Gemini added as primary provider; hackathon mode enforces Gemini-only |
| RD.2 | Google GenAI SDK or ADK | EXISTS — google.genai SDK for Imagen + Gemini LLM + coherence | GAP — uses raw HTTP to Ollama | **EXISTS** | google.genai Client used throughout: Imagen image gen, Gemini LLM router, storyboard coherence |
| RD.3 | GCP deployment + GCP storage | PARTIAL — GKE + Cloud Run scripts exist (`deploy/gke/`, `deploy/cloudrun/`) but not yet deployed | GAP | **PARTIAL** | Cloud Run deployment scripts added (setup-gcp.sh, deploy.sh, cloudbuild.yaml, CD workflow). Awaiting actual deployment — gcloud CLI needed |
| RD.4 | Multimodal I/O (text+image+audio+video) | PARTIAL — text+image+audio narration exist; video stitch pending | PARTIAL — text+image exists | **PARTIAL** | Audio narration via TTS implemented. Live API voice narration + interleaved generation in progress (cn-du8, cn-7lm) |
| RD.5 | Interleaved mixed output stream | PARTIAL — WebSocket streams text progress + final image | GAP | **PARTIAL** | WebSocket exists; need interleaved media milestones |
| RS.1 | Public repo with reproducible spin-up | PARTIAL — Makefile + docker-compose exist | PARTIAL — start.sh exists | **PARTIAL** | Need unified judge-ready README |
| RS.2 | GCP deployment proof | GAP | GAP | **GAP** | No recording/evidence workflow |
| RS.3 | Architecture diagram | GAP | GAP | **GAP** | Mermaid diagrams needed |
| RS.4 | <4 min demo video | GAP | GAP | **GAP** | Demo runbook + recording needed |

---

## Phase 0: Unified Entry + Onboarding

| ID | Requirement | chrono-canvas | neo-mumbai-noir | Verdict | Notes |
|----|------------|---------------|-----------------|---------|-------|
| R0.1 | Mode selection in <=2 clicks | EXISTS — hackathon mode auto-routes to Story Director; normal mode shows both | PARTIAL — has tab-based UI (`unified_ui.py`) with 7 tabs | **EXISTS** | Hackathon mode flag controls auto-redirect; sidebar reorders story-first; mode selection in 1 click |
| R0.2 | One prebuilt template per mode | GAP | GAP | **GAP** | No template/preset system in either project |
| R0.3 | Empty-state guidance | GAP — Generate page has form but no guidance | PARTIAL — Guide tab loads PRD.md | **GAP** | Need onboarding copy with time-to-result messaging |

---

## Phase 1: Core Generation Workflows

| ID | Requirement | chrono-canvas | neo-mumbai-noir | Verdict | Notes |
|----|------------|---------------|-----------------|---------|-------|
| R1.1 | Free-text prompt → image output | EXISTS — `POST /api/generate` with full pipeline | EXISTS — Story tab → extraction → generation | **EXISTS** | Both have this; chrono-canvas is API-backed with persistent records |
| R1.2 | Storyboard: >=3 scene outputs per run | EXISTS — story pipeline generates multi-panel storyboards with coherence check | EXISTS — Storyboard tab assembles multi-scene output | **EXISTS** | Story pipeline produces 3+ panels per run, storyboard coherence node evaluates consistency |
| R1.3 | Portrait: 1 primary output per run | EXISTS — core pipeline produces 1 portrait per generation request | N/A | **EXISTS** | Directly available |
| R1.4 | Export on completed outputs | EXISTS — `GET /api/export/{id}/download` + Export.tsx page | PARTIAL — Gallery tab shows images but no structured export | **EXISTS** | chrono-canvas has full export path |
| FR1 | Both pipelines from one account | EXISTS — portrait + creative_story pipelines both available | N/A | **EXISTS** | Story Director pipeline added with storyboard generation, coherence check, export |
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
| Must use Gemini | EXISTS (primary LLM provider) | GAP | **EXISTS** |
| Must use GenAI SDK/ADK | EXISTS (google.genai throughout) | GAP | **EXISTS** |
| Must use Google Cloud service | PARTIAL (GKE + Cloud Run scripts, not yet deployed) | GAP | **PARTIAL** |
| Multimodal beyond text-only | PARTIAL (text+image+audio; Live API in progress) | PARTIAL (text+image) | **PARTIAL** — video stitch still needed |
| Demo/proof artifacts | GAP | GAP | **GAP** |

---

## Summary Counts

| Verdict | Phase -1 | Phase 0 | Phase 1 | Phase 2 | Phase 3 | NFR | UX | Analytics | Total |
|---------|----------|---------|---------|---------|---------|-----|-----|-----------|-------|
| EXISTS | 2 | 1 | 5 | 2 | 0 | 2 | 1 | 0 | **13** |
| PARTIAL | 2 | 0 | 1 | 2 | 1 | 3 | 1 | 0 | **10** |
| GAP | 4 | 2 | 0 | 2 | 4 | 0 | 2 | 2 | **16** |
| CONFLICT | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | **0** |

**Key Takeaway:** 16 gaps + 10 partial items remain (down from 19 + 12). Closed:
1. **Devpost compliance** — Gemini + GenAI SDK fully integrated (2 gaps → EXISTS). GCP deploy scripts ready, awaiting actual deployment.
2. **Core generation** — Story Director pipeline, storyboard coherence, dual mode all operational.
3. **Remaining gaps** — GCP deployment proof, demo video, monetization/team features, analytics, video stitch.
