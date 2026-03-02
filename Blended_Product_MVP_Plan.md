# Blended Product MVP Plan: Neo-Mumbai Noir + ChronoCanvas (Devpost-Aligned)

## Product Name (working)
**ChronoNoir Live Story Studio**

## 1. MVP Executive Summary
ChronoNoir Live Story Studio combines Neo-Mumbai Noir's storyboarding workflow with ChronoCanvas's auditable generation pipeline, then adapts the product for Devpost's multimodal agent challenge.  
The MVP will be submitted under **Creative Storyteller**: a real-time agent that accepts narrative input and returns interleaved mixed-media output (text + images + audio + short video artifact).  
Core promise: **turn story text into character-consistent, context-grounded story packages that are reviewable and export-ready in one run**.  
Primary users remain indie storytellers and educators, but the immediate success gate is hackathon compliance plus a compelling 4-minute end-to-end demo.

## 2. Devpost Requirement Fit (Must-Pass)
### Mandatory requirements and product response
- **Leverage a Gemini model**: route core narrative/planning tasks to Gemini.
- **Use Google GenAI SDK or ADK**: implement agent orchestration and tool calls with one of these SDK paths.
- **Use at least one Google Cloud service**: deploy backend runtime on GCP and persist outputs in a GCP service.
- **Multimodal input/output beyond text-only**: input supports story text + optional face image; output streams narrative text, generated images, narration audio, and a stitched short video preview.
- **Category compliance (Creative Storyteller)**: use interleaved mixed output in a single cohesive response flow.

### Submission artifacts to plan into MVP
- Public repo with reproducible spin-up instructions
- Proof of Google Cloud deployment (recording and/or code evidence)
- Architecture diagram
- <4 minute demo video with real-time multimodal behavior (no mockups)

## 3. ICP and Jobs-to-be-Done
**ICP 1 (B2C):** Indie storytellers, comic creators, concept artists.  
**JTBD:** Turn a story draft into a consistent multimodal storyboard package fast.

**ICP 2 (B2B-lite):** Teachers and learning designers.  
**JTBD:** Produce engaging, explainable lesson visuals with narration and shareable media.

## 4. Blending Strategy (Chosen)
**Suite strategy** (single brand, dual workflow entry):
- **Story Director Mode** (Neo-Mumbai Noir core: character extraction, reference search, storyboard panels)
- **Historical Lens Mode** (ChronoCanvas core: context grounding, audit/validation, trusted review)

Why this remains best:
- Preserves strongest existing capabilities from both repos
- Gives judges a clear "creative + trust" differentiation
- Enables one unified multimodal demo journey

## 5. MVP Scope (Outcome-Based)
### In scope
- Unified run flow from prompt to exportable multimodal package
- Character extraction and scene planning from narrative input
- Scene image generation with identity consistency support
- Optional face personalization (consent-first flow)
- Validation/provenance summary per run
- Interleaved output stream during run (text updates + media artifacts as they complete)
- Export bundle: panels, narration audio, short video montage, and provenance summary

### Out of scope (MVP)
- Long-form film/video generation
- Enterprise SSO/governance features
- Full billing/workspace commercialization
- Real-time voice interruption support (Live Agents category scope)

## 6. Must-Have User Journeys
1. **Creative Storyteller run**  
Input story -> extract characters/scenes -> generate scene panels -> stream interleaved narrative + visuals -> generate narration -> export media bundle.

2. **Historically grounded explainer run**  
Input historical prompt -> generate context-grounded visuals -> show trust summary -> narrate key points -> export lesson-ready package.

3. **Personalized story variant run**  
Upload face reference -> generate base + personalized variants -> compare outputs -> export selected set with provenance.

## 7. MVP Packaging and Pricing Hypothesis (Post-Hackathon)
### B2C
- **Free:** capped monthly runs, watermark, limited export bundle
- **Plus ($24/mo target):** higher run volume, full bundle exports, no watermark

### B2B-lite
- **Team Starter ($299/mo target):** shared project space, review checkpoints, higher run quotas

Value metric: completed multimodal story packages per month.

## 8. GTM and Demo Plan (First 90 Days)
### Motion
Hackathon-first launch, then PLG creator onboarding with educator pilot outreach.

### Channels
- Build-in-public demos across creator communities
- Educator pilot outreach with "lesson-in-15-minutes" narrative
- Case-study clips from hackathon demo assets

### Launch phases
- **Weeks 1-2: Compliance sprint**  
Gemini + GenAI SDK/ADK integration, GCP deployment baseline, architecture diagram.
- **Weeks 3-4: Demo polish sprint**  
Interleaved output UX, export bundle completion, scripted live demo flow.
- **Weeks 5-8: Beta commercialization prep**  
Waitlist onboarding, pilot packaging, pricing tests.
- **Weeks 9-12: Public beta**  
Open onboarding with creator + educator proof points.

## 9. MVP Success Metrics
**North Star:** Weekly Completed Multimodal Story Packages (WCMSP)

Supporting metrics:
- Activation: % users reaching first export bundle within 20 minutes
- Completion: % runs producing text + image + audio + video artifacts
- Retention: week-4 active rate
- Trust: % exports with validation summary viewed
- Demo-readiness: median full run time for judge scenario

## 10. Key Risks and Assumptions
- Gemini/GenAI migration can be completed without losing current run reliability. *(Confidence: Med)*
- Interleaved output UX can remain simple while adding multiple media types. *(Confidence: Med)*
- Short video artifact quality will be "good enough" for judges even if lightweight (panel montage + narration). *(Confidence: Med)*
- Face personalization remains policy-sensitive and may need strict default-off behavior. *(Confidence: Low)*

## 11. MVP Build Priorities (Devpost-First)
1. Gemini + GenAI SDK/ADK integration in the existing orchestration path
2. Google Cloud deployment path with one-click reproducible runbook
3. Interleaved mixed-media output contract (text/image/audio/video artifacts in one run)
4. Export bundle for judging and replayability (media + provenance)
5. Demo hardening: deterministic prompt set, fallback flows, timing rehearsal

## 12. Judging Criteria (Hackathon Scoring)

### Innovation & Multimodal User Experience (40%)
- Does the project break the "text box" paradigm?
- Does the agent help "See, Hear, and Speak" in a way that feels seamless?
- Does it have a distinct persona/voice?
- Is the experience "Live" and context-aware, or does it feel disjointed and turn-based?

### Technical Implementation & Agent Architecture (30%)
- Does the code effectively utilize the Google GenAI SDK or ADK?
- Is the backend robustly hosted on Google Cloud?
- Is the agent logic sound?
- Does it handle errors gracefully?
- Does the agent avoid hallucinations? Is there evidence of grounding?

### Demo & Presentation (30%)
- Does the video define the problem and solution?
- Is the architecture diagram clear?
- Is there visual proof of Cloud deployment?
- Does the video show the actual software working?

## 13. Validation Plan (Immediate Experiments)
- **Experiment A (compliance):** run 5 end-to-end judged scenarios proving all mandatory requirements
- **Experiment B (output format):** compare "all-at-end" vs "interleaved streaming" for perceived quality/trust
- **Experiment C (narration value):** image-only package vs image+audio+video package engagement test
- **Experiment D (positioning):** "creative director agent" vs "trusted storytelling studio" landing message test
