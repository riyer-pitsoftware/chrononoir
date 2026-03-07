# Gemini Capability Analysis for Hackathon Scoring

**Date**: 2026-03-07
**Hackathon**: Gemini Live Agent Challenge (Creative Storyteller track)
**Judging**: Innovation & Multimodal UX (40%) | Technical Implementation (30%) | Demo & Presentation (30%)

---

## Adoption-Hungry Features (Google wants showcased)

These are features Google is pushing hardest for developer adoption. Showcasing them signals alignment with Google's strategic priorities and will resonate with judges who are likely Google DevRel or product team members.

### 1. Live API (Bidirectional Streaming)
- **What it is**: Real-time, bidirectional streaming API for audio/video/text. Supports voice input, voice output, camera/screen sharing, interruption handling, and function calling mid-stream. The headline feature of this hackathon (it's in the name).
- **Why Google wants it**: The Live API is Google's answer to OpenAI's Realtime API. It launched with Gemini 2.0 and is their most differentiated offering. The hackathon is literally named after it.
- **Integration difficulty**: HIGH. Requires WebSocket-based client, audio handling infrastructure, and a fundamentally different interaction model from request/response. Would need frontend audio capture, backend Live API session management, and streaming response rendering.
- **Impact on judging**: VERY HIGH. The hackathon name is "Gemini Live Agent Challenge." Projects using the Live API will be seen as truly understanding the assignment. The 40% Innovation/UX criteria asks if the experience feels "Live" and context-aware.
- **Our status**: NOT IMPLEMENTED. We use standard generate_content and generate_content_stream.

### 2. Gemini Native Multimodal Output (Interleaved Text + Images)
- **What it is**: Gemini 2.0 Flash can generate interleaved text and images in a single response. One API call returns a mixed stream of text paragraphs and generated images woven together.
- **Why Google wants it**: This is Google's unique differentiator -- no other major model natively interleaves text and image generation in one call. It directly enables the "Creative Storyteller" category requirement for "interleaved mixed output."
- **Integration difficulty**: LOW-MEDIUM. Use `response_modalities=["TEXT", "IMAGE"]` in GenerateContentConfig. The model handles the interleaving. Need frontend rendering of mixed content parts.
- **Impact on judging**: CRITICAL. The hackathon checklist explicitly requires "interleaved mixed output." The submission checklist flags sequential "text then image" as a red flag. This single feature could be the difference between winning and losing.
- **Our status**: NOT IMPLEMENTED. We currently generate text and images in separate pipeline nodes (narration_script -> scene_image_generation). This is exactly the "sequential pipeline disguised as mixed output" pattern the checklist warns against.

### 3. Google Search Grounding
- **What it is**: Built-in tool that lets Gemini ground its responses in real-time Google Search results. Returns cited, factual responses with source URLs. Configured via `tools=[types.Tool(google_search=types.GoogleSearch())]`.
- **Why Google wants it**: Directly combats hallucination (a key judging criterion), showcases Google's unique data advantage, and is trivial to enable. Judges specifically ask: "Does the agent avoid hallucinations? Is there evidence of grounding?"
- **Integration difficulty**: VERY LOW. Literally one parameter added to the generate_content call. The model handles search queries and citation formatting automatically.
- **Impact on judging**: HIGH. Directly addresses the Technical Implementation criteria (30%) around hallucination avoidance and grounding. Currently we use SerpAPI for research -- switching to native Gemini grounding is both simpler and more on-brand.
- **Our status**: NOT IMPLEMENTED. We use SerpAPI for historical research. Switching to Gemini Search grounding would replace an external dependency with a native Gemini capability.

### 4. Function Calling / Tool Use
- **What it is**: Gemini can call developer-defined functions as tools during generation. The model decides when to invoke tools, receives results, and continues generation. Supports parallel function calls.
- **Why Google wants it**: Core agentic capability. The ADK (Agent Development Kit) is built on top of this. Judges ask about "agent logic" soundness.
- **Integration difficulty**: LOW-MEDIUM. Define function schemas, pass as tools to generate_content, handle function call responses, return results. We already have a graph-based agent -- exposing pipeline nodes as callable tools would be natural.
- **Impact on judging**: MEDIUM-HIGH. Shows the agent is making autonomous decisions, not just following a fixed graph. Particularly valuable if combined with Live API for real-time tool orchestration.
- **Our status**: NOT IMPLEMENTED. Our agent uses LangGraph for orchestration, but Gemini itself doesn't use function calling -- it just receives prompts and returns text.

### 5. Gemini 2.5 Flash / Pro (Latest Models)
- **What it is**: Gemini 2.5 Flash (fast, cheap, 1M context) and Gemini 2.5 Pro (best quality, 1M context). 2.5 Flash supports thinking/reasoning. Both support text, vision, audio, and video input.
- **Why Google wants it**: Latest model generation, demonstrates cutting-edge capability. Using older models signals lack of engagement with the platform.
- **Integration difficulty**: NONE. Just change the model string.
- **Impact on judging**: LOW-MEDIUM directly, but using an older model would be a negative signal.
- **Our status**: IMPLEMENTED. We're on `gemini-2.5-flash`. Good.

### 6. Multimodal Input Understanding (Vision + Audio + Video)
- **What it is**: Gemini can understand images, video frames, audio, and PDFs as input. Supports bounding boxes, spatial reasoning, document understanding, and video temporal understanding.
- **Why Google wants it**: Demonstrates Gemini as a universal multimodal reasoner, not just a text model.
- **Integration difficulty**: LOW for images (we already do this), MEDIUM for video/audio input.
- **Impact on judging**: MEDIUM. We already use multimodal input for coherence checking and image-to-story. Adding video understanding would be a nice demo moment.
- **Our status**: PARTIALLY IMPLEMENTED. We send images + text to Gemini for storyboard coherence and reference image analysis. We don't process video or audio as input.

### 7. Imagen 3 via Gemini API
- **What it is**: Image generation through the Gemini API using Imagen models.
- **Why Google wants it**: Keeps image generation within the Google ecosystem.
- **Integration difficulty**: NONE -- already done.
- **Impact on judging**: Already captured.
- **Our status**: IMPLEMENTED. Using `imagen-4.0-fast-generate-001`.

### 8. Text-to-Speech via Gemini
- **What it is**: Generate spoken audio from text using Gemini's built-in TTS with multiple voice options.
- **Why Google wants it**: Multimodal output beyond text, completes the "See, Hear, and Speak" vision.
- **Integration difficulty**: NONE -- already done.
- **Impact on judging**: Already captured.
- **Our status**: IMPLEMENTED. narration_audio node uses Gemini TTS with configurable voices.

---

## Quick Wins for ChronoCanvas

Features we can add with minimal effort that judges will notice, mapped to judging criteria.

| Quick Win | Effort | Criteria Impact | How |
|-----------|--------|-----------------|-----|
| **Google Search Grounding** | 2-4 hours | Technical (30%): grounding, hallucination avoidance | Add `tools=[types.Tool(google_search=types.GoogleSearch())]` to research/context generation calls. Replace SerpAPI dependency. Show citations in UI. |
| **Interleaved Text+Image Output** | 1-2 days | Innovation/UX (40%): breaks text-box, mixed output | Add a "live preview" endpoint that calls Gemini 2.0 Flash with `response_modalities=["TEXT","IMAGE"]` for a single-call story generation. Render mixed parts in frontend. |
| **Agent Persona / Voice** | 4-8 hours | Innovation/UX (40%): persona, voice, context-aware | Add a strong system prompt persona (e.g., "Noir Narrator" character) that persists across the session. Style all text output through this voice. Make it feel like a creative partner, not a pipeline. |
| **Streaming Progress as "Live" Experience** | 1 day | Innovation/UX (40%): feels live, not turn-based | Enhance WebSocket streaming to show agent reasoning, partial text, image generation in-progress indicators, and narration playback as artifacts arrive -- not just a progress bar. |
| **Function Calling for Scene Editing** | 1-2 days | Technical (30%): agent logic, GenAI SDK usage | Let the scene_editor use Gemini function calling to decide which tool to invoke (regenerate image, adjust narration, change style). Shows autonomous agent behavior. |

---

## Features We Already Have

Cross-reference with existing ChronoCanvas capabilities:

| Feature | Gemini Capability Used | Judging Criteria |
|---------|----------------------|------------------|
| **Text generation** (story orchestration, character extraction, scene decomposition, narration scripts) | Gemini 2.5 Flash via google.genai SDK | Technical: GenAI SDK usage |
| **Image generation** (scene images) | Imagen via google.genai SDK | Technical: GenAI SDK, multimodal output |
| **Multimodal validation** (storyboard coherence) | Gemini vision: images + text sent for coherence scoring | Innovation: multimodal UX; Technical: grounding |
| **Image-to-story** (upload image, generate story from it) | Gemini vision: image understanding | Innovation: multimodal input |
| **Reference image analysis** | Gemini vision: analyze uploaded reference images | Innovation: multimodal input |
| **TTS narration** | Gemini TTS with voice selection | Innovation: "Hear" modality |
| **Video assembly** | Pipeline node (moviepy-based montage of panels + audio) | Innovation: "See" modality, mixed media output |
| **Streaming text** | generate_content_stream via google.genai SDK | Innovation: feels live |
| **Cloud deployment** | Cloud Run, Cloud SQL, Memorystore Redis | Technical: GCP hosted |
| **LangGraph agent pipeline** | 12-node state graph with conditional routing | Technical: agent architecture |
| **Audit trail / cost tracking** | LLM call logging, token counting, cost estimation | Technical: error handling, observability |
| **Hackathon mode flag** | HACKATHON_MODE=true forces Gemini-only, story-first UX | Technical: intentional configuration |
| **Coherence-driven regeneration** | Storyboard coherence node can trigger scene re-generation | Technical: agent logic, self-correction |

**Summary**: We already cover Gemini text gen, Imagen, multimodal validation (vision), TTS, streaming, and Cloud Run. Our gaps are: Live API, interleaved output, Google Search grounding, and function calling.

---

## Recommended Additions (Ranked by Effort/Impact)

### Tier 1: Must-Do (High Impact, Low-Medium Effort)

#### 1. Interleaved Text+Image Generation Mode
- **Effort**: 1-2 days
- **Impact**: CRITICAL -- directly addresses the #1 scoring requirement
- **What to build**: A "Live Story" endpoint that sends a prompt to Gemini 2.0 Flash with `response_modalities=["TEXT", "IMAGE"]`. The model returns interleaved text paragraphs and generated images in a single streaming response. Frontend renders them as they arrive -- text appears, then an image materializes, then more text, etc. This is the single most important missing feature.
- **Demo value**: Judge sees one prompt turn into a flowing mixed-media story in real-time. Not "wait for pipeline, see results" but "watch the story unfold live."
- **Risk**: Gemini's native image generation quality may not match Imagen. Mitigation: use this for the "live preview" experience, then offer a "polished export" path that uses the full pipeline with Imagen.

#### 2. Google Search Grounding for Historical Research
- **Effort**: 2-4 hours
- **Impact**: HIGH -- directly addresses hallucination/grounding judging criteria
- **What to build**: In the story_orchestrator or scene_decomposition node, add `tools=[types.Tool(google_search=types.GoogleSearch())]` to the Gemini call config. The model will automatically search for historical context and cite sources. Display citations in the UI and export bundle.
- **Demo value**: Judge sees "Powered by Google Search" citations appearing alongside generated content. Concrete proof of grounding.
- **Risk**: Minimal. Additive change, doesn't break existing flow.

#### 3. Agent Persona ("The Noir Narrator")
- **Effort**: 4-8 hours
- **Impact**: HIGH on Innovation/UX (40%) -- persona/voice is explicitly judged
- **What to build**: A persistent system prompt persona that styles all agent output. The agent introduces itself, narrates its creative process, and speaks in character. Example: "I'm your Noir Narrator. Let me weave this tale for you..." This transforms the pipeline from "processing your request" to "performing your story."
- **Demo value**: Immediately memorable. Judges specifically ask "Does it have a distinct persona/voice?"

### Tier 2: Should-Do (High Impact, Medium Effort)

#### 4. Live API Integration (Voice-Driven Story Direction)
- **Effort**: 3-5 days
- **Impact**: VERY HIGH -- the hackathon is named after this feature
- **What to build**: A "Live Director" mode where the user speaks to the agent via microphone. The agent responds with voice, generating story elements in real-time. Uses the Gemini Live API (WebSocket-based bidirectional streaming). The user can interrupt, redirect, ask questions about the story, and hear the agent think out loud.
- **Demo value**: Maximum wow factor. "Talk to your story" is immediately legible and impressive.
- **Risk**: High complexity. Live API requires WebSocket session management, audio pipeline, and careful UX design. Could be buggy in demo if not well-tested.
- **Recommendation**: Even a simplified version (voice input -> text+image response -> voice readback) would score well. Does not need to be a full bidirectional conversation.

#### 5. Function Calling for Autonomous Scene Editing
- **Effort**: 1-2 days
- **Impact**: MEDIUM-HIGH -- shows agent autonomy and GenAI SDK depth
- **What to build**: Define tools like `regenerate_scene(scene_index, style_adjustment)`, `adjust_narration(scene_index, tone)`, `search_reference(query)`. Pass these to Gemini as function declarations. When the user asks "make scene 3 more dramatic" the agent autonomously decides which tools to call.
- **Demo value**: Shows the agent making decisions, not just following a script. Addresses "agent logic" criteria.

### Tier 3: Nice-to-Have (Lower ROI or Higher Risk)

#### 6. Video Input Understanding
- **Effort**: 1-2 days
- **Impact**: MEDIUM -- additional multimodal input modality
- **What to build**: Allow users to upload a video clip and have Gemini analyze it for story context, characters, setting. Feed the analysis into the story pipeline.
- **Demo value**: "Upload any video, get a noir story based on it" is a cool demo moment.

#### 7. Gemini Thinking/Reasoning Display
- **Effort**: 4-8 hours
- **Impact**: LOW-MEDIUM -- shows model capability but may slow UX
- **What to build**: Enable thinking mode on Gemini 2.5 Flash for complex planning tasks (story orchestration). Show the model's reasoning chain in a collapsible UI panel.
- **Demo value**: Transparency about AI reasoning, aligns with audit/trust narrative.

#### 8. ADK (Agent Development Kit) Migration
- **Effort**: 3-5 days
- **Impact**: MEDIUM on Technical criteria -- shows Google-native agent framework
- **What to build**: Migrate from LangGraph to Google's ADK for agent orchestration. ADK is purpose-built for Gemini agents with native tool use, session management, and multi-agent patterns.
- **Demo value**: "Built with Google ADK" is a strong signal to judges.
- **Risk**: HIGH. Major refactor with limited time. LangGraph works fine. Only worth doing if the team has bandwidth.

---

## Strategic Priority Order (Last 5-7 Days)

Given the judging criteria weights and the FAANG review feedback about being "experience-led not architecture-led":

1. **Day 1-2**: Interleaved text+image generation (Tier 1, #1) -- the single most important gap
2. **Day 2**: Google Search grounding (Tier 1, #2) -- 2-4 hour integration, huge credibility boost
3. **Day 2-3**: Agent persona (Tier 1, #3) -- transforms feel from pipeline to performer
4. **Day 3-5**: Live API voice integration (Tier 2, #4) -- even a basic version scores huge
5. **Day 5-6**: Demo video production -- show working software, not architecture slides
6. **Day 6-7**: README rewrite, Devpost polish, architecture diagram

**Key principle from the FAANG review**: "Stop adding capabilities, start adding experience." Every feature above is chosen not for technical impressiveness but for judge-facing experiential impact.

---

## Gemini Features We Should NOT Invest In

- **Code Execution**: Not relevant to creative storytelling
- **Context Caching**: Optimization feature, invisible to judges
- **Batch API**: Opposite of "live" feel
- **Structured Output / JSON mode**: Already using it, no demo value in highlighting it
- **Fine-tuning**: Not available for latest models, and judges want to see general capability

---

## Bottom Line

The three features Google is most desperate to see adopted -- and that we're missing -- are:

1. **Interleaved multimodal output** (text + images in one response)
2. **Live API** (real-time bidirectional streaming)
3. **Google Search grounding** (built-in factual grounding)

Adding #1 and #3 is achievable in 2 days and would transform our submission from "pipeline that uses Gemini" to "native Gemini creative experience." Adding #2 (even a basic version) would put us in the top tier of submissions because it directly addresses the hackathon's namesake feature.

The existing ChronoCanvas capabilities (TTS, Imagen, multimodal validation, LangGraph pipeline, Cloud Run deployment, audit trail) are strong foundations. The gap is in the *experience layer* -- making the agent feel live, conversational, and creative rather than sequential and mechanical.
