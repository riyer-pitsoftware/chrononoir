# ChronoCanvas Configuration HUD — Design Plan

## Overview

ChronoCanvas has ~40 configuration flags that control which services power each stage of the pipeline. Today these live in `.env` files and are invisible to the user. This plan moves **service selection** into a pre-orchestration UI while keeping **secrets** secure in `.env`.

The UI is a **musician's mixing board** — channels, faders, and signal routing — not a developer settings panel.

---

## Two Modes

### GCP / Remote Mode (Cloud)

Everything runs on cloud APIs. No local services required. Ideal for deployment, demos, and hackathon judging.

| Subsystem | Provider | Required Key (from .env) |
|---|---|---|
| LLM (all tasks) | Gemini | `GOOGLE_API_KEY` |
| Image Generation | Imagen | `GOOGLE_API_KEY` |
| Face Search | SerpAPI Google Images | `SERPAPI_KEY` |
| TTS / Narration | Gemini TTS | `GOOGLE_API_KEY` |
| Multimodal Vision | Gemini Multimodal | `GOOGLE_API_KEY` |
| Stock Images (Neo-Noir) | Pexels + Unsplash | `PEXELS_API_KEY`, `UNSPLASH_ACCESS_KEY` |
| Face Compositing | Disabled | — |
| Research Cache | PostgreSQL + pgvector | (infra, no key) |

**Locked behaviors in GCP mode:**
- `HACKATHON_STRICT_GEMINI=true` — no fallback away from Gemini
- `HACKATHON_MODE=true` — Story Director default
- Ollama, ComfyUI, Stable Diffusion, FaceFusion all grayed out

### Local / Studio Mode (Flexible)

Mix and match local and cloud services per channel. For development, experimentation, and offline work.

Every channel is independently configurable. Any cloud provider can be swapped for a local alternative and vice versa.

---

## The Mixing Board — Channel Architecture

The HUD is organized as a mixing board with **6 channels**. Each channel controls one subsystem. The user selects a mode (GCP or Local) which sets defaults, then can override individual channels.

```
┌─────────────────────────────────────────────────────────────────────┐
│  CHRONOCANVAS SIGNAL CHAIN                            [GCP] [LOCAL] │
├─────────┬─────────┬─────────┬─────────┬─────────┬─────────────────┤
│  LLM    │  IMAGE  │  SEARCH │  VOICE  │  VISION │  COMPOSITING    │
│  ENGINE │  GEN    │  & REF  │  & TTS  │  & MML  │  & POST         │
│         │         │         │         │         │                  │
│ ●Gemini │ ●Imagen │ ●SerpAPI│ ●Gemini │ ●Gemini │ ○FaceFusion     │
│ ○Claude │ ○ComfyUI│ ○Pexels │  TTS    │  MML    │ ●Mock/Off       │
│ ○OpenAI │ ○SD     │ ○Unspla │         │         │                 │
│ ○Ollama │ ○Mock   │ ○Off    │ ○Off    │ ○Off    │                 │
│         │         │         │         │         │                  │
│ [model] │ [model] │         │ [voice] │         │                 │
│ gemini- │ imagen- │         │ Kore    │         │                 │
│ 2.5-    │ 4.0-    │         │         │         │                 │
│ flash   │ fast    │         │         │         │                 │
│         │         │         │         │         │                  │
│  ╔═══╗  │  ╔═══╗  │  ╔═══╗  │  ╔═══╗  │  ╔═══╗  │  ╔═══╗         │
│  ║ ▲ ║  │  ║ ▲ ║  │  ║ ▲ ║  │  ║ ▲ ║  │  ║ ▲ ║  │  ║   ║         │
│  ║ │ ║  │  ║ │ ║  │  ║ │ ║  │  ║ │ ║  │  ║ │ ║  │  ║   ║         │
│  ║ │ ║  │  ║ │ ║  │  ║ │ ║  │  ║ │ ║  │  ║   ║  │  ║   ║         │
│  ╚═══╝  │  ╚═══╝  │  ╚═══╝  │  ╚═══╝  │  ╚═══╝  │  ╚═══╝         │
│  READY  │  READY  │  READY  │  READY  │  READY  │  OFF            │
└─────────┴─────────┴─────────┴─────────┴─────────┴─────────────────┘
         Faders = cost/quality tradeoff    Status LEDs = key present
```

---

## Channel Detail

### Channel 1: LLM Engine

Controls all text generation — research, extraction, prompt writing, validation, orchestration.

| Setting | Env Var | Options | Default (GCP) | Default (Local) |
|---|---|---|---|---|
| Provider | `DEFAULT_LLM_PROVIDER` | `gemini`, `claude`, `openai`, `ollama` | `gemini` | `ollama` |
| Model | `GEMINI_MODEL` / `CLAUDE_MODEL` / `OPENAI_MODEL` / `OLLAMA_MODEL` | see below | `gemini-2.5-flash` | `llama3.1:8b` |
| Strict Gemini | `HACKATHON_STRICT_GEMINI` | on/off | on | off |
| Per-agent routing | `LLM_AGENT_ROUTING` | JSON dict | `{}` | `{}` |
| Rate limit | `RATE_LIMIT_RPM` | 1-600 | 60 | 60 |
| Max concurrent | `LLM_MAX_CONCURRENT` | 1-20 | 5 | 5 |

**Available models per provider:**

| Provider | Models | Cost (input / output per 1M tokens) |
|---|---|---|
| Gemini | `gemini-2.5-flash`, `gemini-2.0-flash`, `gemini-2.0-flash-lite`, `gemini-1.5-flash`, `gemini-1.5-pro` | $0.15/$0.60 (flash) to $1.25/$5.00 (pro) |
| Claude | `claude-sonnet-4-5-20250929`, `claude-haiku-4-5-20251001` | $3.00/$15.00 (sonnet) to $0.80/$4.00 (haiku) |
| OpenAI | `gpt-4o`, `gpt-4o-mini` | $2.50/$10.00 (4o) to $0.15/$0.60 (mini) |
| Ollama | `llama3.1:8b` (or any local model) | Free |

**Per-agent routing (advanced, Local mode only):**

The LLM router supports overriding the provider for specific pipeline agents. This is exposed as an advanced panel (slide-out drawer) on the LLM channel.

Agent names that can be individually routed:
- Portrait pipeline: `orchestrator`, `extraction`, `research`, `face_search`, `prompt_generation`, `image_generation`, `validation`
- Story pipeline: `story_orchestrator`, `character_extraction`, `scene_decomposition`, `scene_prompt_generation`, `scene_image_generation`, `storyboard_coherence`, `storyboard_export`

Example: Route `prompt_generation` to Claude for better creative writing, keep everything else on Gemini.

**Fallback behavior:**
- GCP mode: Gemini-only, no fallback (strict mode)
- Local mode: If preferred provider is unavailable, falls back to first available provider in order
- UI shows a "signal path" indicator: `Gemini -> Claude -> OpenAI -> Ollama`

**Required secrets (from .env):**

| Provider | Key | How to verify |
|---|---|---|
| Gemini | `GOOGLE_API_KEY` | Health check: API responds |
| Claude | `ANTHROPIC_API_KEY` | Health check: API responds |
| OpenAI | `OPENAI_API_KEY` | Health check: API responds |
| Ollama | — (no key) | Health check: `GET /api/tags` on `OLLAMA_BASE_URL` |

---

### Channel 2: Image Generation

Controls portrait and scene image creation.

| Setting | Env Var | Options | Default (GCP) | Default (Local) |
|---|---|---|---|---|
| Provider | `IMAGE_PROVIDER` | `imagen`, `comfyui`, `stable_diffusion`, `mock` | `imagen` | `comfyui` |
| Imagen model | `IMAGEN_MODEL` | `imagen-4.0-fast-generate-001` | default | — |
| ComfyUI model | `COMFYUI_MODEL` | `sdxl`, `flux` | — | `sdxl` |
| ComfyUI checkpoint | `COMFYUI_SDXL_CHECKPOINT` | any .safetensors | — | `juggernautXL_v9.safetensors` |
| Portrait size | `PORTRAIT_WIDTH` x `PORTRAIT_HEIGHT` | any px | 1024x1024 | 1024x1024 |

**Provider comparison:**

| Provider | Location | Cost | Quality | Speed | Prompt Style |
|---|---|---|---|---|---|
| Imagen | Cloud (GCP) | $0.02/image | High | ~5s | Natural language prose |
| ComfyUI + SDXL | Local GPU | Free | High | ~10-30s | Comma-separated tags with weights `(feature:1.2)` |
| ComfyUI + Flux | Local GPU | Free | Very High | ~30-60s | Natural language |
| Stable Diffusion | Local GPU | Free | Medium-High | ~10-20s | Tag-based |
| Mock | Anywhere | Free | Placeholder | Instant | N/A |

**Important:** The prompt generation node (`prompt_generation.py`) automatically selects the correct prompt template based on `IMAGE_PROVIDER`:
- `imagen` -> `IMAGEN_PROMPT_TEMPLATE` (prose, photorealistic, max 250 words)
- `comfyui` / `stable_diffusion` -> `SDXL_PROMPT_TEMPLATE` (tags, weighted, max 200 words)

The user does NOT need to know this — switching the provider fader automatically routes the signal through the correct template.

**Content filter warning:** Imagen blocks prompts about real living people. Historical figures work. The UI should show a warning badge on the Imagen channel when selected.

**Required secrets / endpoints (from .env):**

| Provider | Requirement |
|---|---|
| Imagen | `GOOGLE_API_KEY` |
| ComfyUI | `COMFYUI_API_URL` (default `http://localhost:8188`) |
| Stable Diffusion | `SD_API_URL` (default `http://localhost:7860`) |
| Mock | None |

---

### Channel 3: Search & Reference

Controls how the pipeline finds reference images for portraits and stock images for story scenes.

| Setting | Env Var | Options | Default (GCP) | Default (Local) |
|---|---|---|---|---|
| Face search | `FACE_SEARCH_ENABLED` | on/off | on | on |
| Search provider | (implicit from key) | SerpAPI Google Images | SerpAPI | SerpAPI |
| Pexels (Neo-Noir stock) | `PEXELS_API_KEY` | key present = on | on | optional |
| Unsplash (Neo-Noir stock) | `UNSPLASH_ACCESS_KEY` | key present = on | on | optional |
| Research cache | `RESEARCH_CACHE_ENABLED` | on/off | on | on |
| Cache threshold | `RESEARCH_CACHE_THRESHOLD` | 0.0 - 1.0 | 0.85 | 0.85 |

**Face search flow:**
1. Pipeline extracts figure name from user prompt
2. If `FACE_SEARCH_ENABLED=true` and `SERPAPI_KEY` is set: queries Google Images via SerpAPI
3. Downloads first valid portrait image (max 5MB, validated magic bytes)
4. Image used as reference for portrait generation (and optionally FaceFusion compositing)
5. If disabled or key missing: node skips gracefully, pipeline continues without reference

**Stock image search (Neo-Mumbai-Noir module):**
- Pexels and Unsplash APIs provide stock imagery for story scene backgrounds
- Smart search mode: Ollama extracts visual keywords from AI prompt, feeds to stock APIs
- Currently wired via PYTHONPATH mount in Docker, not directly in backend import chain

**Research cache:**
- pgvector semantic search (384-dim embeddings via `all-MiniLM-L6-v2`)
- Avoids redundant LLM calls for similar historical research queries
- Threshold fader: higher = stricter matching (fewer cache hits, more LLM calls)

**Required secrets (from .env):**

| Service | Key |
|---|---|
| SerpAPI | `SERPAPI_KEY` |
| Pexels | `PEXELS_API_KEY` |
| Unsplash | `UNSPLASH_ACCESS_KEY` |

---

### Channel 4: Voice & TTS

Controls text-to-speech narration for story mode.

| Setting | Env Var | Options | Default (GCP) | Default (Local) |
|---|---|---|---|---|
| TTS enabled | `TTS_ENABLED` | on/off | on | on |
| TTS model | `TTS_MODEL` | Gemini TTS models | `gemini-2.5-flash-preview-tts` | `gemini-2.5-flash-preview-tts` |
| Voice | `TTS_VOICE` | Gemini voice names | `Kore` | `Kore` |
| Voice input | `VOICE_INPUT_ENABLED` | on/off | on | on |

**Note:** TTS uses Gemini directly (not via the LLM router). It requires `GOOGLE_API_KEY` regardless of LLM provider selection. If the user selects Ollama for LLM but wants TTS, they still need the Google key.

The UI should make this dependency visible — a dotted line from the Voice channel to the `GOOGLE_API_KEY` indicator.

---

### Channel 5: Vision & Multimodal

Controls Gemini multimodal features that analyze images (not generate them).

| Setting | Env Var | Options | Default (GCP) | Default (Local) |
|---|---|---|---|---|
| Image-to-Story | `IMAGE_TO_STORY_ENABLED` | on/off | on | on |
| Vision narration | `VISION_NARRATION_ENABLED` | on/off | on | on |
| Storyboard coherence | (always on if Google key present) | auto | on | depends on key |
| Conversation mode | `CONVERSATION_MODE_ENABLED` | on/off | off | off |

**All vision features use Gemini multimodal directly** (not the LLM router). Like TTS, they require `GOOGLE_API_KEY` even if the LLM channel is set to Ollama.

| Feature | What it does |
|---|---|
| Image-to-Story | User uploads an image -> Gemini extracts story concept (title, characters, scenes) |
| Vision narration | Gemini sees the generated panel images + script -> writes narration that references visual details |
| Storyboard coherence | Gemini evaluates character consistency, art style, color palette across all panels |
| Conversation mode | Multi-turn dialogue for iterative story refinement (experimental, off by default) |

---

### Channel 6: Compositing & Post-Processing

Controls face compositing (FaceFusion) and pipeline behavior toggles.

| Setting | Env Var | Options | Default (GCP) | Default (Local) |
|---|---|---|---|---|
| FaceFusion | `FACEFUSION_ENABLED` | on/off | off | off |
| FaceFusion URL | `FACEFUSION_API_URL` | URL | — | `http://localhost:7861` |
| Validation retry | `VALIDATION_RETRY_ENABLED` | on/off | on | on |
| Content moderation | `CONTENT_MODERATION_ENABLED` | on/off | on | on |
| Video assembly | `VIDEO_ASSEMBLY_ENABLED` | on/off | on | on |
| Scene editing | `SCENE_EDITING_ENABLED` | on/off | on | on |

**FaceFusion:** Local-only GPU service that composites a reference face onto a generated portrait. Requires a running FaceFusion server and `FACEFUSION_SOURCE_PATH` pointing to the installation. When disabled, a mock client passes through the generated image unchanged.

---

## Security Model

### Principle: Config in the UI, Secrets in .env

The mixing board **never accepts API keys directly**. Instead:

1. **Keys are deployed in `.env`** before the application starts (standard Docker/K8s secret management)
2. **The UI reads key availability** via a health endpoint — it knows *which* keys are present, not their values
3. **Channel options are constrained** by available keys — if `GOOGLE_API_KEY` is missing, Gemini/Imagen channels show as unavailable (LED off, fader disabled)

### Health Endpoint Extension

The existing `/api/health` endpoint is extended to report service availability:

```json
{
  "status": "healthy",
  "hackathon_mode": true,
  "services": {
    "llm": {
      "gemini": true,
      "claude": false,
      "openai": false,
      "ollama": true
    },
    "image": {
      "imagen": true,
      "comfyui": false,
      "stable_diffusion": false
    },
    "search": {
      "serpapi": true,
      "pexels": true,
      "unsplash": false
    },
    "tts": true,
    "facefusion": false
  }
}
```

The UI reads this on load to light up the status LEDs on each channel. **Keys are never transmitted to the frontend.**

### What the UI sends back

When the user clicks "Start" on the mixing board, the frontend sends a **config payload** with the orchestration request:

```json
{
  "config": {
    "mode": "gcp",
    "llm": {
      "provider": "gemini",
      "model": "gemini-2.5-flash",
      "strict_gemini": true,
      "agent_routing": {}
    },
    "image": {
      "provider": "imagen",
      "model": "imagen-4.0-fast-generate-001",
      "width": 1024,
      "height": 1024
    },
    "search": {
      "face_search": true,
      "research_cache": true,
      "cache_threshold": 0.85
    },
    "voice": {
      "tts_enabled": true,
      "tts_voice": "Kore",
      "voice_input": true
    },
    "vision": {
      "image_to_story": true,
      "vision_narration": true,
      "conversation_mode": false
    },
    "post": {
      "facefusion": false,
      "validation_retry": true,
      "content_moderation": true,
      "video_assembly": true
    }
  }
}
```

This payload contains **only non-secret configuration** — provider names, model names, boolean toggles, numeric thresholds. The backend merges this with the `.env`-sourced secrets to build the final `Settings` object for that orchestration run.

---

## Backend Changes Required

### 1. Per-request Settings Override

Currently `Settings` is a module-level singleton (`config.py:134`). The config payload from the UI must override settings **per orchestration run**, not globally.

**Approach:** Create a `RuntimeConfig` dataclass from the request payload. Thread it through the pipeline via LangGraph state (already has a `config` dict field). Each node reads from runtime config first, falls back to global `Settings`.

```python
@dataclass
class RuntimeConfig:
    """Per-request overrides from the UI mixing board."""
    llm_provider: str | None = None
    llm_model: str | None = None
    image_provider: str | None = None
    # ... etc

    def get(self, key: str, default=None):
        """Return override if set, otherwise default."""
        val = getattr(self, key, None)
        return val if val is not None else default
```

### 2. Service Registry per Request

The service registry (`service_registry.py`) currently creates factories at startup. For per-request config, the factories need to accept a `RuntimeConfig` parameter:

```python
def _image_generator_factory(runtime_config: RuntimeConfig | None = None):
    provider = (runtime_config and runtime_config.image_provider) or settings.image_provider
    # ... select based on provider
```

### 3. Health Endpoint Extension

Extend `/api/health` to include the `services` availability map as shown above. The LLM router already has `check_availability()` — wire it into the health response.

### 4. Validation

The backend must validate the config payload:
- Reject provider selections for which no key exists (e.g., selecting Gemini without `GOOGLE_API_KEY`)
- Reject Local-only providers in GCP mode (ComfyUI, Ollama, FaceFusion)
- Return clear error: `{"error": "GOOGLE_API_KEY not configured", "channel": "llm", "provider": "gemini"}`

---

## Frontend Implementation

### UI Concept: The Signal Chain

The mixing board is rendered as a horizontal strip of channels, each with:

1. **Channel label** — name + icon (at top)
2. **Provider selector** — radio buttons styled as illuminated pushbuttons
3. **Model/config knob** — dropdown styled as a rotary selector
4. **Status LED** — green (key present + reachable), amber (key present, not verified), red (key missing)
5. **Fader** — visual-only cost/quality indicator (not a real slider, computed from selection)

### Mode Switch

A prominent toggle at top-right: **[GCP]** / **[LOCAL]**

Switching modes:
- Animates all faders to new positions
- Enables/disables provider options per channel
- Shows/hides advanced panels (per-agent routing only in Local mode)

### Key Dependency Visualization

Dotted SVG lines connect channels that share a key dependency. Example:
- LLM (Gemini) ── GOOGLE_API_KEY ── Image Gen (Imagen) ── Voice (TTS) ── Vision (Multimodal)

If `GOOGLE_API_KEY` is missing, all four channels light red simultaneously, making the shared dependency obvious.

### Persistence

- Config selections are saved to `localStorage` so the user doesn't reconfigure every session
- "Reset to defaults" button restores mode defaults
- Config is sent with every orchestration request (not assumed from previous)

---

## Implementation Sequence

| Phase | What | Where |
|---|---|---|
| 1 | Extend `/api/health` with service availability map | `backend/api/routes/health.py` |
| 2 | Create `RuntimeConfig` dataclass | `backend/src/chronocanvas/config.py` |
| 3 | Thread `RuntimeConfig` through pipeline state | `agents/graph.py`, `agents/story/graph.py` |
| 4 | Update service registry factories to accept runtime config | `service_registry.py` |
| 5 | Update LLM router to accept per-request provider/model | `llm/router.py` |
| 6 | Add config validation endpoint `POST /api/config/validate` | new route |
| 7 | Build mixing board UI component | `frontend/src/components/ConfigHUD/` |
| 8 | Wire config payload into generation request | `frontend/src/api/` |
| 9 | Add per-agent routing advanced panel (Local mode) | `frontend/src/components/ConfigHUD/AgentRouting.tsx` |
| 10 | Add key dependency visualization (SVG lines) | `frontend/src/components/ConfigHUD/KeyDeps.tsx` |

---

## Decision Matrix — What Happens When

| Scenario | LLM | Image Gen | Search | TTS | Vision |
|---|---|---|---|---|---|
| `.env` has only `GOOGLE_API_KEY` | Gemini | Imagen | OFF (no SerpAPI key) | Gemini TTS | Gemini Multimodal |
| `.env` has only `ANTHROPIC_API_KEY` | Claude | Mock (no image key) | OFF | OFF (needs Google) | OFF (needs Google) |
| `.env` has all cloud keys | User choice | User choice | SerpAPI + Pexels + Unsplash | Gemini TTS | Gemini Multimodal |
| `.env` empty, Ollama running | Ollama | Mock or ComfyUI (local) | OFF | OFF | OFF |
| GCP mode, Google key missing | ERROR: cannot start | ERROR: cannot start | — | — | — |
| Local mode, no keys, no Ollama | ERROR: no LLM available | Mock only | OFF | OFF | OFF |
| Mixed: Google key + Ollama | Fader choice | Fader choice | Depends on SerpAPI key | Gemini TTS | Gemini Multimodal |

---

## Open Questions

1. **Neo-Noir stock image integration** — Pexels/Unsplash are implemented in the `neo-mumbai-noir` module but not directly wired into the chrono-canvas backend pipeline. Should we create a backend adapter, or keep them as neo-noir-only features accessed via PYTHONPATH mount?

2. **Per-agent routing UI complexity** — The 14 agent names are implementation details. Should the advanced panel group them by pipeline stage (Research -> Prompt -> Image -> Validation) instead of exposing raw agent names?

3. **Cost estimation** — The fader concept implies showing estimated cost before orchestration starts. Should we compute and display an estimate based on selected providers and typical token/image counts?

4. **Presets** — Beyond GCP/Local, should we support saved presets? (e.g., "Budget: Ollama + Mock", "Quality: Claude + Imagen", "Hackathon: Gemini everything")
