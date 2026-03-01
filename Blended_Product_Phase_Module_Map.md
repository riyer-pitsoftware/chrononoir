# ChronoNoir MVP Phase Map (Devpost Alignment + Code Reality)

## Integration Decision (recommended)
Use **ChronoCanvas as product shell** (API lifecycle, audit, validation, export, WebSocket progress, deploy scaffolding) and treat **Neo-Mumbai-Noir as creative capability modules** (story extraction, storyboard flow, reference discovery, face-consistency workflows).

## Submission Track Decision
Submit as **Creative Storyteller** (interleaved multimodal output), not Live Agents or UI Navigator.

Why:
- Existing blended capability already centers on narrative-to-visual output.
- ChronoCanvas already streams live progress and has auditable run objects.
- Neo already provides strong story-to-scene authoring and consistency workflows.

## Status Legend
- `EXISTS`: directly implemented
- `PARTIAL`: usable baseline but missing Devpost-specific requirement
- `GAP`: not present

## Phase -1: Devpost Compliance Foundation (new)

### Exists now
- Multimodal baseline pipeline (text input -> image output) with real-time progress streaming.
  - `/Users/riyer/code/chrono-canvas/backend/src/chronocanvas/api/websocket.py`
  - `/Users/riyer/code/chrono-canvas/frontend/src/api/hooks/useGenerationWS.ts`
- GCP deployment scaffolding exists in ChronoCanvas (`deploy/gke` manifests and setup scripts).
  - `/Users/riyer/code/chrono-canvas/deploy/gke/README.md`
  - `/Users/riyer/code/chrono-canvas/deploy/gke/scripts/setup-gcp.sh`

### Gap vs Devpost requirements
- `GAP`: No explicit Gemini-first provider path in active blended plan.
- `GAP`: No explicit use of Google GenAI SDK or ADK in current flow.
- `PARTIAL`: GCP deployment scripts exist, but blended product proof flow (recording + evidence links) is not defined.
- `GAP`: No explicit architecture-diagram deliverable plan in the phase map.

### Build target
- Add Gemini provider path for core narrative/planning nodes.
- Implement orchestration/tool wiring through Google GenAI SDK or ADK.
- Deploy backend to Google Cloud (Cloud Run or GKE path) and store artifacts in GCP-backed storage.
- Add "submission evidence pack" tasks: architecture diagram, deployment proof recording, README reproducibility section.

## Phase 0: Unified Entry + Onboarding

### Exists now
- ChronoCanvas route-based app shell and navigation.
  - `/Users/riyer/code/chrono-canvas/frontend/src/App.tsx`
- Neo-Mumbai-Noir full creative workflow tabs.
  - `/Users/riyer/code/neo-mumbai-noir/unified_ui.py`

### Gap vs blended MVP
- `PARTIAL`: No single mode selector for Story Director vs Historical Lens in one shared frontend flow.
- `GAP`: No "judge-ready quick start" path that guarantees first complete multimodal run quickly.

### Build target
- Add mode switch and template-first onboarding in ChronoCanvas frontend.
- Add "demo presets" with deterministic prompts and expected outputs.

## Phase 1: Core Generation Workflows (Blended Run Model)

### Exists now
- Chrono async generation lifecycle with persistent run records.
  - `/Users/riyer/code/chrono-canvas/backend/src/chronocanvas/api/routes/generation.py`
  - `/Users/riyer/code/chrono-canvas/backend/src/chronocanvas/db/models/request.py`
- Neo story extraction, search, generation, storyboard assembly.
  - `/Users/riyer/code/neo-mumbai-noir/extract_characters.py`
  - `/Users/riyer/code/neo-mumbai-noir/image_search.py`
  - `/Users/riyer/code/neo-mumbai-noir/local_generation_comfy.py`
  - `/Users/riyer/code/neo-mumbai-noir/unified_ui.py`

### Gap vs blended MVP
- `PARTIAL`: Chrono run types are portrait-centric; storyboard run type not first-class.
- `PARTIAL`: Neo storyboard flow is not API-backed as durable run artifacts in Chrono model.
- `GAP`: Unified run artifact contract for text/image/audio/video outputs.

### Build target
- Add run type: `creative_story`.
- Wrap Neo extraction/search/storyboard nodes as Chrono services.
- Persist artifact metadata per run (`panel_image`, `narration_audio`, `preview_video`, `provenance_summary`).

## Phase 2: Interleaved Multimodal Output + Trust

### Exists now
- Live text/progress streaming already present in Chrono.
  - `/Users/riyer/code/chrono-canvas/frontend/src/components/generation/StreamingText.tsx`
- Validation, audit, and review surfaces exist.
  - `/Users/riyer/code/chrono-canvas/backend/src/chronocanvas/api/routes/validation.py`
  - `/Users/riyer/code/chrono-canvas/frontend/src/pages/AuditDetail.tsx`
- Face upload and optional compositing baseline exists.
  - `/Users/riyer/code/chrono-canvas/backend/src/chronocanvas/api/routes/faces.py`

### Gap vs Devpost + MVP
- `GAP`: No interleaved mixed-media response contract (currently progress text + final image pattern).
- `GAP`: No first-class narration audio generation in blended run.
- `GAP`: No short video artifact generation path for storyboard preview.
- `PARTIAL`: Provenance exists in audit view but not as concise, export-ready trust card.

### Build target
- Implement interleaved event stream with multimodal artifact milestones.
- Add narration generation stage and artifact persistence.
- Add lightweight video stitch step from storyboard panels + narration.
- Add compact trust card surfaced pre-export.

## Phase 3: Export + Submission Readiness

### Exists now
- Export endpoint/UI baseline exists.
  - `/Users/riyer/code/chrono-canvas/backend/src/chronocanvas/api/routes/export.py`
  - `/Users/riyer/code/chrono-canvas/frontend/src/pages/Export.tsx`
- Existing automation scripts for generating visual evidence assets.
  - `/Users/riyer/code/chrono-canvas/scripts/record-pipeline-gif.mjs`

### Gap vs Devpost submission
- `PARTIAL`: Export currently focuses on image-first flow, not full submission-ready media bundle.
- `GAP`: No dedicated proof-of-GCP deployment recording checklist/process in product docs.
- `GAP`: No explicit architecture diagram generation/maintenance workflow.
- `GAP`: README spin-up path for judges is not yet mapped as a release gate in blended plan.

### Build target
- Export downloadable bundle containing all run artifacts + summary metadata.
- Add judge-pack checklist and scriptable evidence capture flow.
- Add architecture diagram artifact and keep it versioned with product changes.
- Define final "demo day runbook" with timing and fallback scenarios.

## Phase 4: Post-Submission Commercial Layer (deferred)

### Exists now
- Human review statuses and admin queue baseline in Chrono.
  - `/Users/riyer/code/chrono-canvas/backend/src/chronocanvas/api/routes/admin.py`

### Gap vs commercial roadmap
- `GAP`: Billing/subscriptions/credits/workspaces.
- `GAP`: Team collaboration primitives beyond per-run review.

### Build target
- Reintroduce monetization/workspace roadmap only after submission lock.

## Cross-Cutting Requirement Map (Devpost)

### Must use Gemini
- `GAP` in current blended implementation plan.

### Must use Google GenAI SDK or ADK
- `GAP` in current blended implementation plan.

### Must use Google Cloud service
- `PARTIAL`: deploy scaffolding exists; blended proof + runtime contract not finalized.

### Must provide multimodal input/output beyond text-only
- `PARTIAL`: text+image exists; audio/video interleaving absent.

### Must provide demo/proof artifacts
- `GAP`: no explicit phase gates for architecture diagram + proof recording + judge README.

## Recommended Execution Order (module-level)
1. **Phase -1 compliance closure**
   - Gemini + GenAI SDK/ADK + GCP deployment baseline.
2. **Phase 0/1 blended run integration**
   - Storyboard capabilities behind Chrono run model.
3. **Phase 2 multimodal interleaving**
   - Audio/video artifact generation + trust-card UX.
4. **Phase 3 submission hardening**
   - Judge-pack export, architecture diagram, proof videos, reproducible README.
5. **Phase 4 commercialization (optional post-hackathon)**
   - Credits/plans/workspaces.

## Suggested Epics
- Epic A: Devpost Compliance Foundation (Gemini + GenAI SDK/ADK + GCP)
- Epic B: Story Director Run Type + Artifact Model
- Epic C: Interleaved Multimodal Output (text/image/audio/video)
- Epic D: Submission Pack Automation (demo, architecture, deployment proof)
- Epic E: Post-Submission Monetization Layer
