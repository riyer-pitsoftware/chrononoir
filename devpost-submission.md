# ChronoCanvas — Devpost Submission Draft

## Inspiration

Every story starts as a feeling — a scene you can almost see, a voice you can almost hear. But the jump from idea to visual narrative has always required either artistic skill or a dozen disconnected tools. We wanted to build what Dash, our noir director AI, would call "the kind of joint where you walk in with a whisper and walk out with a film." ChronoCanvas is that joint: speak an idea, and watch it become a storyboard you can hear, see, and refine.

## What it does

ChronoCanvas turns a story idea into a complete visual storyboard in a single, fluid workflow. You can type a prompt, speak it aloud through the Gemini Live API, or upload a photograph — the platform meets you where your idea lives. A 13-node LangGraph pipeline decomposes your concept into scenes, generates illustrated panels with Imagen 4, writes narration, and produces audio with Gemini TTS. Gemini 2.0 Flash weaves text and images together in interleaved output, so the creative flow never breaks. A multimodal coherence reviewer examines every panel for visual consistency across the storyboard. You can then refine any scene through natural-language conversation with full image context, listen to Dash narrate your story in real time via the Live API, and export the final result as an MP4 with Ken Burns transitions — all from one interface.

## How we built it

- **Gemini 2.5 Flash** for story decomposition, scene prompting, and streaming text generation
- **Gemini 2.0 Flash** for interleaved text+image output (mandatory track feature)
- **Gemini multimodal vision** for storyboard coherence review, image-to-story extraction, reference image analysis, and vision-enhanced narration
- **Gemini Live API** for voice input (speak your story idea) and live voice narration of panels
- **Gemini TTS** (voice: Kore) for narration audio generation
- **Imagen 4** (`imagen-4.0-fast-generate-001`) for scene illustration
- **Google Search grounding** for historical research with citations
- **Google GenAI SDK** (`google-genai`) as the unified client for all Gemini and Imagen calls
- **LangGraph StateGraph** orchestrating a 13-node pipeline with real-time WebSocket progress streaming
- **ARQ + Redis** for async job queue and pub/sub event delivery
- **PostgreSQL** for generation state, audit trail with per-call cost tracking, and validation results
- **React 18 + Vite** frontend with live WebSocket panel rendering
- **Docker Compose** for local development; **Cloud Run** deployment scripts with Cloud SQL and Memorystore Redis
- **Infrastructure-as-code**: `deploy/cloudrun/scripts/setup-gcp.sh` provisions all GCP resources; `deploy.sh` builds, pushes, and deploys three Cloud Run services

## Challenges we ran into

- **Content filtering at scale.** Imagen 4's safety filters block prompts involving real people, which is exactly what a historical storytelling tool needs. We built a research-grounding layer with Google Search so the model works with verified historical context rather than raw name-drops, and we added graceful retry logic when filters trigger mid-pipeline.
- **Coherence across generated panels.** Each scene image is generated independently, so character appearance and art style can drift across a storyboard. We added a dedicated Gemini multimodal coherence node that reviews all panels together, flags inconsistencies, and annotates scenes for targeted regeneration — turning a six-image consistency problem into a single multimodal evaluation.
- **Keeping the pipeline recoverable.** A 13-node pipeline with multiple external API calls has many failure points. LangGraph's state graph made it possible to checkpoint progress and resume from the last successful node, but wiring that through an async worker queue with WebSocket status updates required careful orchestration.

## Accomplishments that we're proud of

- **Seven distinct Gemini integrations in one pipeline.** Text generation, multimodal vision, interleaved output, image generation, TTS, Live API, and Search grounding all work together in a single user flow — not as isolated demos, but as stages in one coherent pipeline.
- **Real-time creative feedback loop.** Users see panels stream in over WebSocket, can chat with Gemini about their storyboard with the actual images as context, and hear Dash narrate the result — all without leaving the page. The gap between "idea" and "watchable storyboard" is under two minutes.
- **Full cost transparency.** Every Gemini and Imagen call is logged with token counts, latency, and cost. The audit trail is not a compliance checkbox — it is how we tuned the pipeline to stay under budget during development.

## What we learned

- **Interleaved output changes the design contract.** When Gemini can return text and images in a single response, the frontend can no longer assume "one request, one content type." We had to rethink our rendering pipeline to handle mixed-media chunks arriving in sequence — a pattern that will become standard as multimodal models mature.
- **Multimodal evaluation is more useful than multimodal generation.** The coherence reviewer — where Gemini looks at all six panels and critiques them together — turned out to be the highest-value node in the pipeline. Generating images is easy; knowing which ones are wrong is the hard part.
- **GenAI SDK unification pays off.** Using `google-genai` as a single client for Gemini, Imagen, and Search grounding eliminated an entire class of credential-management and version-compatibility bugs. One SDK, one API key, seven capabilities.

## What's next for ChronoCanvas

- **Collaborative storyboarding.** Multiple users contributing scenes to the same storyboard in real time, with Gemini mediating style consistency across contributors.
- **Audio design and soundtrack.** Extending beyond TTS narration to ambient sound and AI-generated music scored to the mood of each scene.
- **Long-form narrative.** Scaling from single storyboards to multi-chapter visual novels with persistent characters, arc tracking, and continuity enforcement across dozens of scenes.
