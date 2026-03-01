# Architecture Diagrams: ChronoNoir Studio

> Generated 2026-02-28 | Phase 2 Architecture

## 1. Docker Compose Service Topology

```mermaid
graph TB
    subgraph "Docker Compose Stack"
        subgraph "frontend-net"
            FE["frontend<br/>:3000 (Nginx/Vite)"]
            API["api<br/>:8000 (FastAPI)"]
        end

        subgraph "db-net"
            DB[("db<br/>PostgreSQL 16 + pgvector<br/>:5432")]
            REDIS[("redis<br/>:6379")]
        end

        subgraph "worker-net"
            WORKER["worker<br/>(ARQ)"]
        end

        subgraph "llm-net"
            NEO["noir-pipeline<br/>:7860 (Gradio)"]
        end
    end

    subgraph "Host Processes (GPU)"
        OLLAMA["Ollama<br/>:11434"]
        COMFYUI["ComfyUI<br/>:8188"]
        FF["FaceFusion<br/>:7870"]
    end

    subgraph "Cloud APIs"
        CLAUDE["Anthropic Claude"]
        OPENAI["OpenAI GPT-4o"]
        GEMINI["Google Gemini"]
        PEXELS["Pexels"]
        UNSPLASH["Unsplash"]
        SERPAPI["SerpAPI"]
    end

    FE -->|HTTP/WS| API
    API -->|async jobs| REDIS
    REDIS -->|dequeue| WORKER
    API --> DB
    WORKER --> DB
    WORKER -->|host.docker.internal| OLLAMA
    WORKER -->|host.docker.internal| COMFYUI
    WORKER -->|host.docker.internal| FF
    WORKER --> CLAUDE
    WORKER --> OPENAI
    WORKER --> GEMINI
    WORKER --> SERPAPI

    NEO -->|host.docker.internal| OLLAMA
    NEO -->|host.docker.internal| COMFYUI
    NEO -->|host.docker.internal| FF
    NEO --> PEXELS
    NEO --> UNSPLASH
```

## 2. Data Flow: Journey J1 — Creative Storyteller Run

```mermaid
sequenceDiagram
    participant U as User (Browser)
    participant FE as React Frontend
    participant API as FastAPI API
    participant WS as WebSocket
    participant W as ARQ Worker
    participant LG as LangGraph Pipeline
    participant PG as PostgreSQL
    participant R as Redis
    participant Gem as Gemini
    participant OL as Ollama
    participant CUI as ComfyUI
    participant FF as FaceFusion

    U->>FE: Select Story Director mode
    U->>FE: Enter story text + optional face
    FE->>API: POST /api/generate {mode: creative_story, text, face_id?}
    API->>PG: Create generation_request (status: pending)
    API->>R: Enqueue run_generation_pipeline
    API-->>FE: 202 {request_id}

    FE->>WS: Connect /ws/generation/{request_id}

    W->>R: Dequeue job
    W->>LG: Execute pipeline

    LG->>OL: Orchestrator: plan execution
    R-->>WS: Progress: "Planning story structure..."
    WS-->>FE: Stream update

    LG->>Gem: Extract characters + scenes from story
    R-->>WS: Progress: "Extracting characters..."

    LG->>Gem: Research historical/narrative context
    R-->>WS: Progress: "Researching context..."

    loop For each scene (>=3)
        LG->>Gem: Generate scene prompt
        LG->>CUI: Generate scene image
        R-->>WS: Progress: {type: "image", url: "/output/scene_N.png"}
        LG->>PG: Save generated_image record
    end

    opt Face provided
        loop For each scene image
            LG->>FF: Swap face into scene
            R-->>WS: Progress: {type: "image", url: "/output/scene_N_personalized.png"}
        end
    end

    LG->>Gem: Validate outputs (score 0-100)
    LG->>PG: Save validation_results

    Note over LG: Future: narration audio + video stitch

    LG->>PG: Update request status: completed
    R-->>WS: Progress: {type: "complete", artifacts: [...]}
    WS-->>FE: Final results with all artifacts
```

## 3. Data Flow: Journey J2 — Historical Portrait Run

```mermaid
sequenceDiagram
    participant U as User
    participant FE as React Frontend
    participant API as FastAPI API
    participant W as ARQ Worker
    participant LG as LangGraph Pipeline
    participant PG as PostgreSQL
    participant Gem as Gemini
    participant CUI as ComfyUI
    participant FF as FaceFusion

    U->>FE: Select Historical Lens mode
    U->>FE: Enter historical figure/prompt + optional face
    FE->>API: POST /api/generate {mode: historical_portrait, text, face_id?}
    API->>PG: Create generation_request
    API-->>FE: 202 {request_id}

    W->>LG: Execute pipeline
    LG->>Gem: Extract figure details
    LG->>Gem: Research historical context (clothing, appearance, era)
    LG->>Gem: Generate image prompt from research
    LG->>CUI: Generate portrait
    LG->>Gem: Validate portrait (historical accuracy score)

    opt Score < 70
        LG->>Gem: Regenerate prompt
        LG->>CUI: Regenerate image
        LG->>Gem: Re-validate
    end

    opt Face provided
        LG->>FF: Composite face onto portrait
    end

    LG->>PG: Save all artifacts + audit trail
    LG-->>FE: Complete with validation summary + provenance
```

## 4. Deployment Layout (Single Machine)

```mermaid
graph LR
    subgraph "Docker Engine"
        subgraph "Containers"
            FE["Frontend :3000"]
            API["API :8000"]
            WORKER["Worker"]
            DB["PostgreSQL :5432"]
            REDIS["Redis :6379"]
            NEO["Noir Pipeline :7860"]
        end
        subgraph "Shared Volumes"
            VOL_OUT[("output/")]
            VOL_UP[("uploads/")]
            VOL_PG[("pgdata/")]
        end
    end

    subgraph "Host Machine"
        OLLAMA["Ollama :11434<br/>(llama3.1:8b, llama3.2)"]
        COMFYUI["ComfyUI :8188<br/>(SDXL/FLUX)"]
        FF["FaceFusion :7870<br/>(inswapper_128 + gfpgan)"]
        GPU["GPU (CUDA/MPS)"]
    end

    COMFYUI --> GPU
    FF --> GPU
    OLLAMA -.-> GPU

    API --> VOL_OUT
    API --> VOL_UP
    WORKER --> VOL_OUT
    NEO --> VOL_OUT
    DB --> VOL_PG
```
