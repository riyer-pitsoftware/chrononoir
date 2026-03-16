# ChronoCanvas — Project Story

> *Walk in with a whisper. Walk out with a film.*
> A multimodal Gemini pipeline that turns text, voice, or images into narrated visual stories.

---

## Inspiration

I've always loved noir. Not just the films — the books, the voice, the moral ambiguity, the way a good noir story makes you lean in even when you know the setup is a trap. Hammett, Chandler, Kurosawa's *Stray Dog*, the rain-soaked alleyways of *Casablanca*. Noir is a way of seeing the world: high contrast, low trust, and a story that won't let you look away.

What I kept imagining were noir stories in places you'd never expect them. A detective story set in British India during World War II. Hansel and Gretel reimagined in 1930s Chicago. A jazz musician in 1940s New Orleans who finds a photograph of himself taken thirty years before he was born. The genre has this incredible flexibility — drop it into any era, any culture, and the shadows still work. But I could never *see* these stories. I could write them, but the visual side — the panels, the lighting, the faces — stayed locked in my head.

That frustration became ChronoCanvas. Not "what can AI generate?" but "can I finally see the noir stories I've been carrying around?"

The project grew out of Neo-Mumbai-Noir, an earlier experiment in noir storytelling. That project gave me Dash — named after Dashiell Hammett, the Pinkerton detective who invented hardboiled fiction. Dash became the creative director at the center of ChronoCanvas: a persona who doesn't just generate content but has opinions about it. He'll push back on a scene that's too clean. He'll tell you noir isn't about pretty — it's about the thing your character doesn't want to say. Building a tool wasn't enough. I wanted a collaborator who understood the genre.

## What It Does

ChronoCanvas turns a story idea into a complete illustrated, narrated storyboard — and it meets you wherever your idea starts.

**Type a prompt**, and a 13-node LangGraph pipeline decomposes it into scenes, generates illustrated panels with Imagen 4, writes narration with the actual images as context, and synthesizes audio with Gemini TTS. The whole thing streams live over WebSocket — panels appear one by one as they generate.

**Speak to Dash** through the Live Noir Session, and he narrates back in real time via the Gemini Live API. Mid-conversation, he triggers function calls to generate scene images that materialize on screen while he keeps talking. No buttons, no menus — voice is the interface.

**Watch it unfold** in Live Story mode, where Gemini streams interleaved text and images in a single response — paragraphs of noir prose arriving alongside illustrated scenes, rendered with typewriter animation, camera iris reveals, and film dissolve transitions.

A multimodal coherence reviewer examines all panels together, scores five consistency dimensions, and triggers selective regeneration when characters drift. You can refine any scene through natural-language conversation with full image context. When it's done, export the result as a narrated MP4 with Ken Burns transitions.

## How We Built It

ChronoCanvas started as a much bigger application. The original version was a full historical portrait studio — a timeline spanning 500 BCE to 1700 CE, a figure library with 102 historical characters, a 9-node LangGraph pipeline for generating historically-accurate portraits with face compositing, an evaluation framework, admin panels, validation queues. It supported four LLM providers, multiple image generators, and had deployment manifests for both Cloud Run and GKE.

Then the hackathon requirements landed: Creative Storyteller track, Gemini Live API, interleaved output, hosted on Google Cloud. The challenge wasn't building something new — it was cutting the existing product down to its sharpest edge. We stripped the UI to three pages (Story Director, Live Story, Live Session), locked the backend to Gemini-only routing, and focused entirely on the live storytelling experience. The timeline, the figure library, the portrait pipeline, the multi-provider routing — all still there under the hood, but hidden behind a hackathon mode flag that activates when deployed to GCP. What remained was the part that mattered: speak a story, watch it appear, hear it narrated.

Underneath the hackathon surface, ChronoCanvas is provider-agnostic. A smart LLM router supports four providers — Gemini, Claude, OpenAI, and Ollama for fully local models — with per-agent routing so you can run scene decomposition on Gemini but prompt generation on Claude if you prefer the output. Image generation routes through Imagen, ComfyUI (local Stable Diffusion workflows on port 8188), or a direct Stable Diffusion provider. FaceFusion handles face compositing via ONNX models in a Docker container. A ConfigHUD — modeled after a musician's mixing board with six channels (LLM, Image, Search, Voice/TTS, Vision/Multimodal, Compositing) — lets you switch providers per-request from the UI. In local studio mode, you can run the entire pipeline offline with Ollama and ComfyUI, no API keys required.

For the hackathon, all of that collapses to Gemini. The `google-genai` SDK serves as the single client for seven capabilities: text generation, multimodal vision, interleaved output, image generation, TTS, Live API, and Search grounding. Strict Gemini mode blocks fallback to other providers and returns a clean 503 if Gemini is unavailable — no silent routing surprises during a demo.

The infrastructure runs on Google Cloud: three Cloud Run services (API, worker, frontend), Cloud SQL for PostgreSQL, Memorystore for Redis, and GCS for artifact storage. Deployment is scripted end-to-end — `deploy-all.sh` provisions all GCP resources, builds containers, and deploys in one pass.

Every Gemini and Imagen call is logged with token counts, latency, provider, and cost. The audit trail isn't a compliance feature — it's how we tuned the pipeline. When a 13-node pipeline makes 20+ API calls per generation, you need to see exactly where time and money go.

## Challenges We Ran Into

**Scoping a bigger product down to a focused hackathon entry.** ChronoCanvas had four LLM providers, multiple image generators, a historical timeline, a figure library, an eval framework, and admin panels. The hackathon required Gemini Live API and interleaved output on Google Cloud. The hardest design decision wasn't what to build — it was what to hide. We built a hackathon mode that activates on GCP deployment: the sidebar collapses to three pages, provider routing locks to Gemini, and the landing page drops you straight into the Story Director. The full application is still deployable for local development, but the hackathon surface is ruthlessly focused on live storytelling. Cutting features you've already built is harder than not building them in the first place.

**Gemini's thinking tokens consume the output budget.** Gemini 2.5 Flash's internal reasoning counts against `max_output_tokens`, which meant our JSON responses were getting truncated mid-object — closing braces simply never arrived. We built a shared `json_repair` module with eight recovery strategies, including a truncation repair that detects unclosed brackets and reconstructs valid JSON from partial responses. Every node in the story pipeline routes through it.

**Content filtering at scale.** Imagen 4's safety filters block prompts involving real people — exactly the kind of prompts a historical storytelling tool generates. We added Google Search grounding so the model works with verified historical context rather than raw name references, and built a three-tier image fallback chain (Gemini 3.1 Flash → Gemini 2.5 Flash with reference images → Imagen 4) so a blocked prompt doesn't stall the pipeline.

**Coherence across independently generated panels.** Each scene image is generated in its own API call, so character appearance and art style drift across a storyboard. The coherence reviewer — where Gemini examines all panels together as a single multimodal input — turned out to be the highest-value node in the pipeline. It scores five dimensions (character consistency, style uniformity, color harmony, narrative flow, continuity tracking) and triggers targeted regeneration of the worst-scoring scenes. Generating images is straightforward; knowing which ones are wrong is the hard part.

**The Live API has sharp edges.** `send_client_content` cannot mix with `send_realtime_input`. Sending `audio_stream_end=True` permanently kills the audio stream. Mixing `google_search` with `function_declarations` causes WebSocket error 1011. The receive loop returns a per-turn async generator — you have to re-call `session.receive()` for each new turn, not loop over a single generator. Each of these cost hours to diagnose because they fail silently or with generic error codes. We documented every constraint so the next developer doesn't repeat them.

**Making streaming feel cinematic, not technical.** Raw SSE events updating a div is a developer demo. We wanted the experience to feel like watching a film develop in a darkroom. That meant narration-gated transitions (scenes don't advance until audio is ready to play), prefetch pipelines that invisibly load the next scene's narration while the current one plays, and film dissolve animations between panels. The technical challenge wasn't streaming — it was making streaming disappear.

## Accomplishments That We're Proud Of

**Seven Gemini integrations in one user flow.** Text generation, multimodal vision, interleaved output, image generation, TTS, Live API, and Search grounding — not as isolated demos, but as stages in a single creative pipeline. One SDK, one API key, one coherent experience.

**The scoping discipline.** Taking a full-featured application and cutting it down to three focused pages without breaking anything underneath. Hackathon mode isn't a separate app — it's a curated view of the same codebase. Flip the flag and the full studio comes back.

**Dash has a personality.** The noir director voice isn't a gimmick layered on top — it's woven into system prompts, narration scripts, loading states, and the Live Session's conversational style. ChronoCanvas doesn't feel like a pipeline with a theme. It feels like a creative partner who happens to run on Gemini.

**Real-time creative feedback loop.** Users see panels stream in live, can speak to Dash and hear him narrate back, refine scenes through conversation with full image context, and export a finished film — all without leaving the interface. The gap between "idea" and "watchable storyboard" is under two minutes.

## What We Learned

**Interleaved output changes the frontend contract.** When Gemini returns text and images in a single response, the renderer can no longer assume one request produces one content type. We had to build a streaming parser that handles mixed-media chunks arriving in unpredictable order — text, then image, then more text — and renders each piece as it lands. This pattern will become standard as multimodal models mature.

**Multimodal evaluation beats multimodal generation.** The coherence reviewer — where Gemini looks at all generated panels and critiques them as a set — consistently delivered more value than any generation node. It's easy to generate six images. Knowing which two need to be redone, and why, is the capability that makes a pipeline production-quality.

**One SDK, seven capabilities.** Using `google-genai` as a single client for everything eliminated an entire class of credential-management and version-compatibility bugs. We hit SDK-level issues (a regression in v1.67 that broke multi-turn thinking chats), but the unified surface area meant each fix applied everywhere.

**The gap between "works" and "feels right" is where the product lives.** ChronoCanvas worked after the pipeline was done. It became a product when we added the iris animation, the typewriter effect, the narration gating, and the film dissolve. None of those are technically necessary. All of them are why people watch the demo twice.

## What's Next for ChronoCanvas

**Collaborative storyboarding.** Multiple users contributing scenes to the same storyboard in real time, with Gemini mediating style consistency across contributors.

**Audio design and soundtrack.** Moving beyond TTS narration to ambient sound and AI-generated music scored to the mood of each scene — rain on a tin roof for the alley scene, a muted trumpet for the jazz club.

**Long-form narrative.** Scaling from single storyboards to multi-chapter visual novels with persistent characters, arc tracking, and continuity enforcement across dozens of scenes. The coherence reviewer already works at the single-storyboard level — the architecture is ready to stretch.

**More genres, same bones.** The pipeline doesn't know it's noir. Dash does. Swap the persona, adjust the visual grammar, and ChronoCanvas becomes a western, a gothic horror, a Bollywood thriller. The shadows change shape, but the structure holds.
