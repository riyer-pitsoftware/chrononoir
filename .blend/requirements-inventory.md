# Requirements Inventory: ChronoNoir Studio MVP

> Auto-extracted from blended folder docs on 2026-02-28

## Product Vision

**ChronoNoir Studio** combines cinematic storyboarding (Neo-Mumbai Noir) with auditable, historically grounded portrait generation (ChronoCanvas) into a single product. MVP goal: allow creators and educators to generate exportable, character-consistent, context-grounded visuals in one unified workflow within 20 minutes.

**Submission Track:** Creative Storyteller (Devpost multimodal agent challenge)
**Core Promise:** Turn story text into character-consistent, context-grounded story packages that are reviewable and export-ready in one run.

## Target Users

- **ICP 1 (B2C):** Indie storytellers, comic creators, concept artists, game writers
- **ICP 2 (B2B-lite):** Educators, learning designers, museum/heritage program teams

---

## Phase -1: Devpost Compliance Foundation

### Functional Requirements
| ID | Requirement | Type | Source |
|----|------------|------|--------|
| RD.1 | Route core narrative/planning tasks to Gemini model | Functional | MVP_Plan §2 |
| RD.2 | Implement agent orchestration with Google GenAI SDK or ADK | Functional | MVP_Plan §2 |
| RD.3 | Deploy backend runtime on GCP and persist outputs in GCP service | Functional | MVP_Plan §2 |
| RD.4 | Support multimodal input (text + optional face image) and output (text + images + audio + video) | Functional | MVP_Plan §2 |
| RD.5 | Category compliance: interleaved mixed output in single cohesive response flow | Functional | MVP_Plan §2 |

### Submission Artifacts
| ID | Requirement | Type | Source |
|----|------------|------|--------|
| RS.1 | Public repo with reproducible spin-up instructions | Submission | MVP_Plan §2 |
| RS.2 | Proof of Google Cloud deployment (recording and/or code evidence) | Submission | MVP_Plan §2 |
| RS.3 | Architecture diagram | Submission | MVP_Plan §2 |
| RS.4 | <4 minute demo video with real-time multimodal behavior (no mockups) | Submission | MVP_Plan §2 |

---

## Phase 0: Unified Entry + Onboarding

### Requirements
| ID | Requirement | Type | Source |
|----|------------|------|--------|
| R0.1 | User can select a mode in <=2 clicks from first screen | UX | PRD §6 |
| R0.2 | User can start from one prebuilt template per mode | UX | PRD §6 |
| R0.3 | Empty-state guidance explains expected output and time-to-result | UX | PRD §6 |

### Acceptance Criteria
| ID | Criterion | Source |
|----|----------|--------|
| AC0.1 | New user can reach generation form in <=60 seconds | PRD §6 |
| AC0.2 | At least one template run in each mode produces a valid output payload | PRD §6 |
| AC0.3 | Onboarding copy includes safety and usage guardrails | PRD §6 |

---

## Phase 1: Core Generation Workflows (MVP Core)

### Requirements
| ID | Requirement | Type | Source |
|----|------------|------|--------|
| R1.1 | User can submit free-text prompt/story and receive generated image output | Functional | PRD §6 |
| R1.2 | Storyboard mode produces at least 3 scene outputs per run | Functional | PRD §6 |
| R1.3 | Portrait mode returns one primary portrait output per run | Functional | PRD §6 |
| R1.4 | Export action available immediately on completed outputs | Functional | PRD §6 |

### Acceptance Criteria
| ID | Criterion | Source |
|----|----------|--------|
| AC1.1 | 95% of valid submissions complete without blocking errors | PRD §6 |
| AC1.2 | Median time prompt->first output <=8 minutes in standard environment | PRD §6 |
| AC1.3 | Exported files are downloadable and include run metadata (run id, timestamp, mode) | PRD §6 |

---

## Phase 2: Trust Layer + Personalization

### Requirements
| ID | Requirement | Type | Source |
|----|------------|------|--------|
| R2.1 | Every completed output includes a readable validation summary block | Functional | PRD §6 |
| R2.2 | Every output includes provenance summary: steps completed + generation context | Functional | PRD §6 |
| R2.3 | User can upload one face image and attach it to a generation request | Functional | PRD §6 |
| R2.4 | When face provided, system returns both original and personalized output (or clear fallback reason) | Functional | PRD §6 |
| R2.5 | Compare view shows original and personalized versions in one screen | UX | PRD §6 |

### Acceptance Criteria
| ID | Criterion | Source |
|----|----------|--------|
| AC2.1 | 100% of exportable outputs show validation summary | PRD §6 |
| AC2.2 | Face upload supports JPEG/PNG <=10MB with user-visible validation messages | PRD §6 |
| AC2.3 | If personalization fails, original output remains exportable and failure reason is displayed | PRD §6 |
| AC2.4 | Users can export original-only, personalized-only, or both | PRD §6 |

---

## Phase 3: Monetization + Team Starter

### Requirements
| ID | Requirement | Type | Source |
|----|------------|------|--------|
| R3.1 | Credit usage decremented per generation run and visible in UI | Functional | PRD §6 |
| R3.2 | Free plan enforces monthly credit cap and watermark policy | Functional | PRD §6 |
| R3.3 | Plus plan removes watermark and increases credit allowance | Functional | PRD §6 |
| R3.4 | Team Starter supports shared project access for up to 10 seats | Functional | PRD §6 |
| R3.5 | Team project includes review statuses: Draft, In Review, Approved | Functional | PRD §6 |

### Acceptance Criteria
| ID | Criterion | Source |
|----|----------|--------|
| AC3.1 | Billing plan state correctly changes generation limits within 1 minute of upgrade | PRD §6 |
| AC3.2 | Free-limit exceeded events show upgrade CTA and no silent failure | PRD §6 |
| AC3.3 | Team members can view shared outputs and update review status with audit timestamp | PRD §6 |

---

## Cross-Cutting Functional Requirements

| ID | Requirement | Type | Source |
|----|------------|------|--------|
| FR1 | System must support both mode-specific pipelines from one account | Functional | PRD §7 |
| FR2 | Each generation run must create a persistent run record | Functional | PRD §7 |
| FR3 | Users must be able to revisit prior outputs and re-export | Functional | PRD §7 |
| FR4 | Output cards must display mode, completion time, and export state | UX | PRD §7 |
| FR5 | Safety/usage policy notice must be shown before first face-personalized run | Compliance | PRD §7 |

---

## Non-Functional Requirements

| ID | Requirement | Type | Source |
|----|------------|------|--------|
| NFR1 | Availability target during MVP beta: 99.0% weekly uptime | Availability | PRD §8 |
| NFR2 | 95th percentile generation status updates visible to users within 3 seconds of state change | Performance | PRD §8 |
| NFR3 | System should handle at least 50 concurrent active generation sessions in beta | Concurrency | PRD §8 |
| NFR4 | User-facing errors must include actionable next step text | UX | PRD §8 |
| NFR5 | Audit/provenance records retained for at least 30 days in MVP | Data | PRD §8 |

---

## UX Requirements

| ID | Requirement | Type | Source |
|----|------------|------|--------|
| UX1 | First-run experience must provide "quick start" and "advanced" paths | UX | PRD §9 |
| UX2 | Progress states must use plain-language step labels | UX | PRD §9 |
| UX3 | Result page must prioritize primary CTA: Export | UX | PRD §9 |
| UX4 | Compare view for personalization must be accessible on desktop and mobile | UX | PRD §9 |

---

## Analytics & Instrumentation

### Required Events
| Event | Source |
|-------|--------|
| `mode_selected` | PRD §10 |
| `generation_submitted` | PRD §10 |
| `generation_completed` | PRD §10 |
| `validation_summary_viewed` | PRD §10 |
| `export_clicked` | PRD §10 |
| `face_upload_success` | PRD §10 |
| `face_upload_failed` | PRD §10 |
| `plan_upgrade_clicked` | PRD §10 |
| `plan_upgraded` | PRD §10 |

### Required Event Properties
`user_id`, `run_id`, `mode`, `plan_type`, `completion_time_sec`, `output_count`, `export_type`

---

## MVP User Journeys

| # | Journey | Source |
|---|---------|--------|
| J1 | Creative Storyteller run: Input story -> extract characters/scenes -> generate scene panels -> stream interleaved narrative + visuals -> generate narration -> export media bundle | MVP_Plan §6 |
| J2 | Historically grounded explainer run: Input historical prompt -> generate context-grounded visuals -> show trust summary -> narrate key points -> export lesson-ready package | MVP_Plan §6 |
| J3 | Personalized story variant run: Upload face reference -> generate base + personalized variants -> compare outputs -> export selected set with provenance | MVP_Plan §6 |

---

## Success Metrics

| Metric | Target | Source |
|--------|--------|--------|
| North Star: Weekly Shareable Outputs (WSO) | Growth | PRD §5 |
| Activation: first export within 20 min | >=35% | PRD §5 |
| Retention: week-4 active users | >=25% | PRD §5 |
| Monetization: free->paid conversion | >=4% | PRD §5 |
| Trust usage: exports with validation summary viewed | >=60% | PRD §5 |
| Completion: runs producing text+image+audio+video artifacts | Growth | MVP_Plan §9 |

---

## Non-Goals (Explicit)

- Video generation (long-form)
- Enterprise governance/SSO
- Public marketplace ecosystem
- Real-time voice interruption support
- Full billing/workspace commercialization (deferred post-hackathon)
