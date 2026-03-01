# Build Map: ChronoNoir Studio

> Generated 2026-02-28 | Phase 2 Architecture

## Requirement → Build Action Mapping

### Phase -1: Devpost Compliance

| Requirement | Build Action | Target | Dependencies | Priority | Bead |
|------------|-------------|--------|--------------|----------|------|
| RD.1 | Add GeminiProvider class following LLMProvider ABC. Add `google-genai` to pyproject.toml. Wire into LLMRouter with GOOGLE_API_KEY + GEMINI_MODEL config. | chrono-canvas | None | P0 | history-faces-dr4 |
| RD.2 | Implement GenAI SDK integration. Option A: use google-genai SDK as the Gemini provider backend. Option B: use ADK for agent orchestration (replaces LangGraph for Devpost). Recommend Option A (minimal change). | chrono-canvas | RD.1 | P0 | history-faces-slj |
| RD.3 | Update GKE manifests for blended product. Add Cloud Storage bucket for artifacts. Create deployment runbook with proof-capture steps. | chrono-canvas | R1.2 | P1 | history-faces-egu |
| RD.4a | Add narration audio generation: integrate TTS API (Google Cloud TTS or local). New pipeline node after validation. Persist as run artifact. | chrono-canvas | R1.2 | P1 | history-faces-gcr |
| RD.4b | Add video stitch: ffmpeg-based montage from scene panels + narration. New pipeline node. Persist as run artifact. | chrono-canvas | RD.4a | P1 | history-faces-6yb |
| RD.5 | Extend WebSocket event contract to emit interleaved artifact milestones. Emit image URLs as they generate, not just final batch. | chrono-canvas | R1.2 | P1 | history-faces-wv3 |
| RS.1 | Unified README with one-command spin-up for judges. Cover host service setup + docker compose. | chrono-canvas | All Phase -1 | P1 | history-faces-dwn |
| RS.2 | GCP deployment proof: scripted recording, screenshot capture, deployment log. | chrono-canvas | RD.3 | P1 | history-faces-jh1 |
| RS.3 | Architecture diagram: mermaid source + rendered PNG. Versioned in repo. | chrono-canvas | RD.3 | P1 | history-faces-jh1 |
| RS.4 | Demo runbook: deterministic prompt set, timing marks, fallback scenarios. Record <4 min video. | chrono-canvas | All | P1 | history-faces-jh1 |

### Phase 0: Unified Entry + Onboarding

| Requirement | Build Action | Target | Dependencies | Priority | Bead |
|------------|-------------|--------|--------------|----------|------|
| R0.1 | Add ModeSelector component to React frontend. Two cards: "Story Director" and "Historical Lens". Route to Generate page with mode param. | chrono-canvas | None | P1 | history-faces-nf2 |
| R0.2 + R0.3 + UX1 | Add template gallery per mode. Preset prompts with expected outputs. Empty-state guidance with time-to-result. Quick start vs advanced paths. | chrono-canvas | R0.1 | P2 | history-faces-64f |

### Phase 1: Core Generation Workflows

| Requirement | Build Action | Target | Dependencies | Priority | Bead |
|------------|-------------|--------|--------------|----------|------|
| R1.2 + FR1 | Add `creative_story` run type to generation_requests model. Build storyboard LangGraph subgraph: orchestrator → extraction → search → prompt_gen (x N scenes) → image_gen (x N) → validation → compositing → export. | chrono-canvas | Neo API services | P1 | history-faces-iq5 |
| R1.2 (Neo) | Expose `extract_characters()` + `generate_search_queries()` as importable Python functions or FastAPI endpoints callable from chrono-canvas worker. | neo-mumbai-noir | None | P1 | neo-mumbai-noir-rft |
| R1.2 (Neo) | Expose `ImageSearcher` + `SmartImageSearcher` as callable service. Accept queries, return structured results. | neo-mumbai-noir | None | P1 | neo-mumbai-noir-qc1 |
| R1.2 (Neo) | Expose storyboard assembly as callable service. Accept characters + scene images, return structured storyboard JSON. | neo-mumbai-noir | neo-mumbai-noir-rft | P1 | neo-mumbai-noir-n77 |
| FR4 | Add `mode` field to output cards in AuditList and generation list views. | chrono-canvas | R0.1 | P2 | — (minor, covered by R0.1) |
| Integration | Unified Docker Compose merging both projects. Shared output volume. Standardized env vars. | chrono-canvas | R0.1, Neo APIs | P1 | history-faces-21f |
| Integration | Migrate Neo data models (characters, scenes, stories, images, face_swaps) to PostgreSQL via Alembic migration. | chrono-canvas | Neo APIs | P1 | history-faces-s3i |

### Phase 2: Trust + Personalization

| Requirement | Build Action | Target | Dependencies | Priority | Bead |
|------------|-------------|--------|--------------|----------|------|
| R2.2 | Build compact TrustCard component. Shows: pipeline steps completed, validation score, LLM providers used, generation time, cost. Surfaced pre-export. | chrono-canvas | None | P2 | history-faces-0qn |
| R2.4 + R2.5 + UX4 | Modify facial_compositing node to preserve original image alongside composited. Add CompareView component (side-by-side, responsive). Export selector: original/personalized/both. | chrono-canvas | None | P2 | history-faces-0ov |
| FR5 | Add ConsentModal component. Shown on first face upload. Stores consent state. Blocks generation until accepted. | chrono-canvas | R2.3 (exists) | P2 | history-faces-21y |
| Analytics | Integrate analytics SDK (PostHog, Mixpanel, or custom). Fire 9 required events with required properties. | chrono-canvas | R0.1 | P2 | history-faces-1b9 |

### Phase 3: Monetization + Team

| Requirement | Build Action | Target | Dependencies | Priority | Bead |
|------------|-------------|--------|--------------|----------|------|
| R3.1-R3.3 | Add credit system: credits table, decrement per run, plan-based limits, watermark logic. Stripe or Lemon Squeezy integration for Plus plan. | chrono-canvas | None | P3 | history-faces-www |
| R3.4-R3.5 | Add workspace/team model: users, teams, memberships, shared projects. Review status enum: Draft/In Review/Approved. | chrono-canvas | R3.1 | P3 | history-faces-ukf |

---

## Build Action Summary by Target Project

### chrono-canvas (17 build actions)
- Phase -1 compliance: 10 actions (Gemini, GenAI SDK, GCP, audio, video, streaming, README, proof, diagram, demo)
- Phase 0 onboarding: 2 actions (mode selector, templates)
- Phase 1 core: 3 actions (creative_story run type, unified docker, DB migration)
- Phase 2 trust: 4 actions (trust card, compare view, consent, analytics)
- Phase 3 monetization: 2 actions (credits, team workspace)

### neo-mumbai-noir (3 build actions)
- Phase 1 core: 3 actions (extraction API, search API, storyboard API)

### Key Architectural Decision: Integration Pattern

**Chosen: Direct Python import** (not HTTP microservice)

The chrono-canvas worker and neo-mumbai-noir modules run in the same Python environment. Rather than neo-mumbai-noir exposing HTTP endpoints that chrono-canvas calls, the worker directly imports and calls Neo's Python functions:

```python
# In chrono-canvas worker / LangGraph node
from neo_modules.extract_characters import extract_characters
from neo_modules.image_search import ImageSearcher, SmartImageSearcher
```

**Why:**
- Same Python 3.11 version
- Avoids inter-container HTTP overhead
- Simpler error handling and tracing
- Neo's functions are already cleanly factored (pure functions with clear inputs/outputs)

**How:**
- Neo modules packaged as installable Python package or added to PYTHONPATH
- Neo's Gradio UI continues to run independently for standalone use
- Shared `output/` volume for image files
