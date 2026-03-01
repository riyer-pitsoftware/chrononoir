# Shared Contracts: ChronoNoir Studio

> Generated 2026-02-28 | Phase 2 Architecture

## 1. Run Type Contract

The `generation_requests` table gains a `mode` field to distinguish pipelines:

```
mode: "historical_portrait" | "creative_story"
```

**historical_portrait** — existing chrono-canvas pipeline (single portrait output)
**creative_story** — new storyboard pipeline (multi-scene output, uses Neo modules)

Both modes share: request lifecycle, WebSocket progress, audit trail, export, validation.

---

## 2. Generation Request Schema (Extended)

```json
{
  "request_id": "uuid",
  "mode": "creative_story | historical_portrait",
  "input_text": "story text or historical prompt",
  "face_id": "uuid | null",
  "status": "pending | processing | completed | failed",
  "extracted_data": {
    // historical_portrait: { name, era, region, role, physical_description }
    // creative_story: { characters: [...], scenes: [...] }
  },
  "research_data": { /* historical context or narrative enrichment */ },
  "generated_prompt": "string | null",
  "artifacts": [
    {
      "type": "panel_image | portrait | narration_audio | preview_video | provenance_summary",
      "file_path": "/output/...",
      "scene_index": 0,       // for storyboard scenes
      "is_personalized": false,
      "metadata": {}
    }
  ],
  "validation_score": 0-100,
  "agent_trace": [ /* LangGraph step log */ ],
  "llm_costs": { "total_usd": 0.0, "by_provider": {} },
  "created_at": "ISO-8601",
  "completed_at": "ISO-8601 | null"
}
```

---

## 3. WebSocket Progress Events (Extended)

Current chrono-canvas pattern: `{"status", "agent", "message", "data"}`

Extended for interleaved multimodal:

```json
// Text progress
{"type": "progress", "agent": "extraction", "message": "Extracting characters from story..."}

// Image artifact ready (NEW)
{"type": "artifact", "artifact_type": "panel_image", "scene_index": 0, "url": "/output/scene_0.png", "is_personalized": false}

// Audio artifact ready (FUTURE)
{"type": "artifact", "artifact_type": "narration_audio", "url": "/output/narration.mp3"}

// Video artifact ready (FUTURE)
{"type": "artifact", "artifact_type": "preview_video", "url": "/output/preview.mp4"}

// Validation result
{"type": "validation", "score": 85, "summary": "..."}

// Run complete
{"type": "complete", "request_id": "uuid", "artifacts": [...]}
```

---

## 4. Character Extraction Contract (Neo → Chrono)

When chrono-canvas API invokes Neo's character extraction:

**Input:**
```json
{
  "story_text": "Full narrative text",
  "ollama_model": "llama3.2"  // or routed to Gemini
}
```

**Output:**
```json
{
  "characters": [
    {
      "name": "string",
      "slug": "string",
      "age": "string",
      "ethnicity": "string",
      "gender": "string",
      "facial_features": ["string"],
      "clothing": "string",
      "key_scenes": [
        {
          "scene_key": "string",
          "scene_name": "string",
          "description": "string"
        }
      ],
      "emotions": ["string"]
    }
  ],
  "search_queries": [
    {
      "character_slug": "string",
      "query_type": "base_portrait | emotion | scene",
      "query_text": "string"
    }
  ]
}
```

This maps directly from Neo's `extract_characters.py` output + `generate_search_queries()`.

---

## 5. Image Search Contract (Neo → Chrono)

**Input:**
```json
{
  "queries": [
    {"query_text": "string", "per_page": 5, "orientation": "portrait"}
  ]
}
```

**Output:**
```json
{
  "results": [
    {
      "query": "string",
      "images": [
        {
          "id": "string",
          "source": "pexels | unsplash",
          "url": "string",
          "thumbnail_url": "string",
          "photographer": "string",
          "alt": "string"
        }
      ]
    }
  ]
}
```

---

## 6. Storyboard Assembly Contract

**Input:**
```json
{
  "request_id": "uuid",
  "characters": [ /* from extraction */ ],
  "scene_images": [
    {"scene_key": "string", "file_path": "string", "personalized_path": "string | null"}
  ]
}
```

**Output:**
```json
{
  "storyboard": {
    "title": "string",
    "panels": [
      {
        "scene_index": 0,
        "scene_key": "string",
        "description": "string",
        "character_names": ["string"],
        "image_path": "string",
        "personalized_image_path": "string | null"
      }
    ]
  }
}
```

---

## 7. Export Bundle Contract

**Single-mode export (current):**
```
{request_id}/
├── portrait.png
└── metadata.json
```

**Storyboard export (new):**
```
{request_id}/
├── scene_0.png
├── scene_0_personalized.png  (optional)
├── scene_1.png
├── scene_2.png
├── narration.mp3             (future)
├── preview.mp4               (future)
├── provenance.json
└── metadata.json
```

**metadata.json** includes: request_id, mode, timestamps, character data, validation scores, LLM costs, export variant (original/personalized/both).

---

## 8. LLM Provider Interface (Gemini Addition)

New provider follows existing `LLMProvider` ABC:

```python
class GeminiProvider(LLMProvider):
    name = "gemini"

    async def generate(
        self,
        prompt: str,
        system_prompt: str | None = None,
        temperature: float = 0.7,
        max_tokens: int = 2000,
        json_mode: bool = False,
    ) -> LLMResponse: ...
```

Router addition:
```python
self.providers["gemini"] = GeminiProvider()
```

Routing for Devpost compliance:
```python
DEFAULT_ROUTING = {
    TaskType.EXTRACTION: "gemini",       # Devpost requirement
    TaskType.RESEARCH: "gemini",         # Devpost requirement
    TaskType.PROMPT_GENERATION: "gemini", # Devpost requirement
    TaskType.VALIDATION: "gemini",       # Devpost requirement
    TaskType.ORCHESTRATION: "ollama",    # local, fast
    TaskType.GENERAL: "ollama",
}
```
