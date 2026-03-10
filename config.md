# ChronoCanvas ConfigHUD -- Operator Manual

The ConfigHUD is your mixing board for ChronoCanvas. It controls which services power each stage of the pipeline -- from writing to image generation to narration. Think of it as a signal chain: your story prompt flows through six channels, each with its own provider, model, and settings.

API keys live in your `.env` file and are never entered through the UI. The ConfigHUD reads which keys are available and lights up each channel accordingly.

---

## Modes

### GCP Mode (Cloud)

Everything runs on Google Cloud APIs. No local hardware required. One key (`GOOGLE_API_KEY`) powers most of the board.

When GCP mode is active:
- Gemini is locked in as the LLM provider (no fallback)
- Story Director is the default experience
- Local-only providers (Ollama, ComfyUI, FaceFusion) are grayed out

### Local Mode (Studio)

Mix and match cloud and local services freely. Run an LLM on your own machine, generate images with a local GPU, or blend local and cloud providers across channels. Every channel is independently configurable.

---

## The Six Channels

### Channel 1: LLM Engine

Controls all text generation -- research, character extraction, prompt writing, scene decomposition, validation.

| Provider | Key Required | Models | Approximate Cost |
|---|---|---|---|
| Gemini | `GOOGLE_API_KEY` | gemini-2.5-flash, gemini-2.0-flash, gemini-1.5-pro | $0.15 - $5.00 per 1M tokens |
| Claude | `ANTHROPIC_API_KEY` | claude-sonnet-4-5, claude-haiku-4-5 | $0.80 - $15.00 per 1M tokens |
| OpenAI | `OPENAI_API_KEY` | gpt-4o, gpt-4o-mini | $0.15 - $10.00 per 1M tokens |
| Ollama | None (local) | llama3.1:8b or any installed model | Free |

**Fallback behavior:**
- In GCP mode, Gemini is the only option. If it fails, the pipeline stops.
- In Local mode, if your preferred provider is unavailable, the system tries the next one in order: Gemini, Claude, OpenAI, Ollama.

**Per-agent routing (Local mode only):** An advanced panel lets you assign different providers to individual pipeline stages. For example, you could route creative prompt writing through Claude while keeping everything else on Gemini.

### Channel 2: Image Generation

Controls portrait and scene image creation.

| Provider | Key / Endpoint Required | Speed | Style |
|---|---|---|---|
| Imagen | `GOOGLE_API_KEY` | ~5 seconds | Photorealistic, natural language prompts |
| ComfyUI + SDXL | `COMFYUI_API_URL` (local GPU) | ~10-30 seconds | High quality, tag-based prompts with weights |
| ComfyUI + Flux | `COMFYUI_API_URL` (local GPU) | ~30-60 seconds | Very high quality, natural language prompts |
| Stable Diffusion | `SD_API_URL` (local GPU) | ~10-20 seconds | Tag-based prompts |
| Mock | None | Instant | Placeholder images for testing |

When you switch providers, the prompt style adjusts automatically. Imagen gets prose descriptions; ComfyUI and Stable Diffusion get weighted tags. You do not need to change your input.

**Imagen content filter:** Imagen blocks prompts about real living people. Use historical figures instead.

### Channel 3: Search & Reference

Controls how the pipeline finds reference images and research material.

| Service | Key Required | What It Does |
|---|---|---|
| SerpAPI | `SERPAPI_KEY` | Finds portrait reference photos via Google Images |
| Pexels | `PEXELS_API_KEY` | Provides stock imagery for scene backgrounds |
| Unsplash | `UNSPLASH_ACCESS_KEY` | Additional stock imagery source |

**Face search:** When enabled, the pipeline looks up a reference photo of the person in your prompt and uses it to guide portrait generation. If the key is missing or search is turned off, the pipeline continues without a reference -- it still works, just with less visual accuracy.

**Research cache:** Stores previous historical research results so repeated queries for similar figures skip the LLM call. The cache threshold slider controls how strict the matching is -- higher means fewer cache hits and fresher results, lower means more reuse.

### Channel 4: Voice & TTS

Controls text-to-speech narration for stories.

| Setting | What It Does |
|---|---|
| TTS on/off | Enables spoken narration of your story panels |
| Voice selector | Choose the narrator voice (default: Kore) |
| Voice input | Speak your prompts instead of typing |

Voice always runs through Gemini TTS, regardless of which LLM provider you chose in Channel 1. This means you need `GOOGLE_API_KEY` for narration even if your LLM is set to Ollama.

### Channel 5: Vision & Multimodal

Controls features that analyze images using Gemini's multimodal capabilities.

| Feature | What It Does |
|---|---|
| Image-to-Story | Upload a photo and Gemini extracts a story concept from it -- title, characters, scenes |
| Vision narration | Gemini sees your generated panels and writes narration that references specific visual details |
| Storyboard coherence | After all panels are generated, Gemini checks character consistency, art style, and color palette across the full storyboard |
| Conversation mode | Multi-turn dialogue for iterative story refinement (experimental, off by default) |

Like Voice, all Vision features require `GOOGLE_API_KEY` regardless of your LLM channel setting.

### Channel 6: Compositing & Post-Processing

Controls face compositing and pipeline behavior.

| Setting | What It Does |
|---|---|
| FaceFusion | Composites a reference face onto a generated portrait (requires local GPU and FaceFusion server) |
| Validation retry | Re-runs quality checks if the first pass flags issues |
| Content moderation | Screens generated content before delivery |
| Video assembly | Assembles story panels into a video sequence |
| Scene editing | Allows editing individual scenes after generation |

FaceFusion is local-only and off by default. When disabled, generated portraits pass through unchanged.

---

## Key Dependencies at a Glance

Most channels share a single key. Here is what lights up with each key present:

| Key in `.env` | Channels Enabled |
|---|---|
| `GOOGLE_API_KEY` | LLM (Gemini), Image Gen (Imagen), Voice (TTS), Vision (all features), Storyboard Coherence |
| `ANTHROPIC_API_KEY` | LLM (Claude) |
| `OPENAI_API_KEY` | LLM (OpenAI) |
| `SERPAPI_KEY` | Search (face reference lookup) |
| `PEXELS_API_KEY` | Search (stock scene imagery) |
| `UNSPLASH_ACCESS_KEY` | Search (stock scene imagery) |

If a key is missing, the corresponding provider appears unavailable on the board -- its status LED goes red and the option is disabled.

---

## Common Configurations

| Setup | What You Need | Result |
|---|---|---|
| Google key only | `GOOGLE_API_KEY` | Gemini for text, Imagen for images, TTS and Vision active, no reference search |
| Google + SerpAPI | `GOOGLE_API_KEY`, `SERPAPI_KEY` | Full cloud pipeline with face reference search |
| All cloud keys | All keys above | Every channel available, choose freely |
| Offline with Ollama | Ollama running locally | LLM via Ollama, Mock or ComfyUI for images, no TTS/Vision/Search |
| Hybrid | `GOOGLE_API_KEY` + Ollama | Use Gemini for TTS/Vision, Ollama for LLM, mix image providers |

---

## How It Works

1. Your `.env` file provides the API keys before the application starts.
2. On load, the ConfigHUD checks which keys are present and marks each channel as available or unavailable.
3. You select a mode (GCP or Local), which sets sensible defaults across all channels.
4. Override any individual channel as needed.
5. Your selections are saved locally so you do not need to reconfigure each session.
6. When you start a generation, your channel settings travel with the request -- the backend uses them for that run without changing the global configuration.
