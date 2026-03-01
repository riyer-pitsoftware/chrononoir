# PRD: ChronoNoir Studio MVP

## 1. Document Control
- Version: 1.0
- Date: 2026-02-28
- Status: Draft (Build-ready)
- Product: ChronoNoir Studio
- Source inputs: `neo-mumbai-noir`, `chrono-canvas`, `Blended_Product_MVP_Plan.md`

## 2. Product Summary
ChronoNoir Studio combines two proven workflows:
- Story-to-storyboard generation with character consistency
- Historically grounded portrait generation with validation/audit context

MVP goal: allow creators and educators to generate exportable, character-consistent, context-grounded visuals in one unified workflow within 20 minutes.

## 3. Goals and Non-Goals
### Goals
- Reduce time from prompt to first shareable output
- Increase trust through visible validation/provenance summaries
- Prove willingness to pay with creator self-serve and team-starter pilots

### Non-Goals
- Video generation
- Enterprise governance/SSO
- Public marketplace ecosystem

## 4. Target Users
- B2C: indie storytellers, concept artists, comic/game creators
- B2B-lite: educators and learning designers

## 5. MVP Success Metrics
- North Star: Weekly Shareable Outputs (WSO)
- Activation: first export within 20 minutes (target: >=35%)
- Retention: week-4 active users (target: >=25%)
- Monetization: free->paid conversion (target: >=4%)
- Trust usage: % exports with validation summary viewed (target: >=60%)

## 6. Release Phasing

## Phase 0: Unified Entry + Onboarding
### Scope
- Single landing/generate entrypoint with mode selection:
  - Storyboard Mode
  - Historical Portrait Mode
- Template-first onboarding with example prompts

### Requirements
- R0.1: User can select a mode in <=2 clicks from first screen.
- R0.2: User can start from one prebuilt template per mode.
- R0.3: Empty-state guidance explains expected output and time-to-result.

### Acceptance Criteria
- AC0.1: New user can reach generation form in <=60 seconds.
- AC0.2: At least one template run in each mode produces a valid output payload.
- AC0.3: Onboarding copy includes safety and usage guardrails.

## Phase 1: Core Generation Workflows (MVP Core)
### Scope
- Storyboard flow (text -> character extraction -> scene outputs)
- Portrait flow (text -> historical context-informed output)
- Export image output from either flow

### Requirements
- R1.1: User can submit free-text prompt/story and receive generated image output.
- R1.2: Storyboard mode produces at least 3 scene outputs per run.
- R1.3: Portrait mode returns one primary portrait output per run.
- R1.4: Export action available immediately on completed outputs.

### Acceptance Criteria
- AC1.1: 95% of valid submissions complete without blocking errors.
- AC1.2: Median time prompt->first output <=8 minutes in standard environment.
- AC1.3: Exported files are downloadable and include run metadata (run id, timestamp, mode).

## Phase 2: Trust Layer + Personalization
### Scope
- Validation summary visible before export
- Provenance/audit snapshot per output
- Optional face upload and face-personalized output variant
- Side-by-side compare: original vs personalized

### Requirements
- R2.1: Every completed output includes a readable validation summary block.
- R2.2: Every output includes provenance summary: steps completed + generation context.
- R2.3: User can upload one face image and attach it to a generation request.
- R2.4: When face is provided, system returns both original and personalized output (or clear fallback reason).
- R2.5: Compare view shows original and personalized versions in one screen.

### Acceptance Criteria
- AC2.1: 100% of exportable outputs show validation summary.
- AC2.2: Face upload supports JPEG/PNG <=10MB with user-visible validation messages.
- AC2.3: If personalization fails, original output remains exportable and failure reason is displayed.
- AC2.4: Users can export original-only, personalized-only, or both.

## Phase 3: Monetization + Team Starter
### Scope
- Credit metering and plan gating
- Free + Plus self-serve plans
- Team Starter workspace basics (shared projects, simple review state)

### Requirements
- R3.1: Credit usage decremented per generation run and visible in UI.
- R3.2: Free plan enforces monthly credit cap and watermark policy.
- R3.3: Plus plan removes watermark and increases credit allowance.
- R3.4: Team Starter supports shared project access for up to 10 seats.
- R3.5: Team project includes review statuses: Draft, In Review, Approved.

### Acceptance Criteria
- AC3.1: Billing plan state correctly changes generation limits within 1 minute of upgrade.
- AC3.2: Free-limit exceeded events show upgrade CTA and no silent failure.
- AC3.3: Team members can view shared outputs and update review status with audit timestamp.

## 7. Functional Requirements (Cross-Cutting)
- FR1: System must support both mode-specific pipelines from one account.
- FR2: Each generation run must create a persistent run record.
- FR3: Users must be able to revisit prior outputs and re-export.
- FR4: Output cards must display mode, completion time, and export state.
- FR5: Safety/usage policy notice must be shown before first face-personalized run.

## 8. Non-Functional Requirements
- NFR1: Availability target during MVP beta: 99.0% weekly uptime.
- NFR2: 95th percentile generation status updates visible to users within 3 seconds of state change.
- NFR3: System should handle at least 50 concurrent active generation sessions in beta.
- NFR4: User-facing errors must include actionable next step text.
- NFR5: Audit/provenance records retained for at least 30 days in MVP.

## 9. UX Requirements
- UX1: First-run experience must provide “quick start” and “advanced” paths.
- UX2: Progress states must use plain-language step labels.
- UX3: Result page must prioritize primary CTA: Export.
- UX4: Compare view for personalization must be accessible on desktop and mobile.

## 10. Analytics and Instrumentation
### Events
- `mode_selected`
- `generation_submitted`
- `generation_completed`
- `validation_summary_viewed`
- `export_clicked`
- `face_upload_success`
- `face_upload_failed`
- `plan_upgrade_clicked`
- `plan_upgraded`

### Required properties
- user_id, run_id, mode, plan_type, completion_time_sec, output_count, export_type

## 11. Risks and Mitigations
- Risk: users perceive product as two disconnected tools.
  - Mitigation: unified onboarding, shared result model, single export surface.
- Risk: trust messaging increases friction.
  - Mitigation: concise summaries first, details on-demand.
- Risk: face personalization policy concerns.
  - Mitigation: explicit consent UX and restricted defaults.

## 12. Dependencies
- Stable generation services for both pipelines
- Face personalization service availability for optional flow
- Usage metering + entitlement checks
- Persistent storage for outputs and run summaries

## 13. Launch Readiness Checklist
- L1: End-to-end run succeeds in both modes
- L2: Export path tested for all output variants
- L3: Plan gating verified (Free/Plus/Team Starter)
- L4: Instrumentation dashboards live for north-star and funnel metrics
- L5: Safety notices and policy links present in personalization flow
- L6: Pilot support playbook ready (onboarding + issue triage)

## 14. Open Questions
- OQ1: Which segment is launch hero: creators or educators?
- OQ2: Should Team Starter include fixed seats or pooled credits first?
- OQ3: What minimum validation summary detail is enough for trust without adding friction?

## 15. Implementation Order Recommendation
1. Phase 0 + Phase 1 (single cohesive beta)
2. Phase 2 trust layer (required before broad public launch)
3. Phase 3 monetization and team features (pilot-to-revenue conversion)
