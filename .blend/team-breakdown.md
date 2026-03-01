# Team Breakdown: ChronoNoir Studio

> Generated 2026-02-28 | Phase 3 Task Refinement

## chrono-canvas (19 beads)

### By Priority
| Priority | Count | IDs |
|----------|-------|-----|
| P0 | 2 | dr4, slj |
| P1 | 11 | egu, gcr, 6yb, wv3, iq5, nf2, 21f, s3i, jh1, dwn, 1b9* |
| P2 | 5 | 0ov, 0qn, 64f, 21y, 1b9 |
| P3 | 2 | www, ukf |

### By Phase
| Phase | Count | IDs |
|-------|-------|-----|
| Phase -1 (Devpost) | 6 | dr4, slj, egu, jh1, dwn, + integration items |
| Phase 0 (Onboarding) | 2 | nf2, 64f |
| Phase 1 (Core) | 1 | iq5 |
| Phase 2 (Trust) | 6 | gcr, 6yb, wv3, 0qn, 0ov, 21y |
| Phase 3 (Monetize) | 2 | www, ukf |
| Integration | 2 | 21f, s3i |

### By Type
| Type | Count |
|------|-------|
| feature | 13 |
| task | 6 |

### Blocked Tasks
| Bead | Blocked By | Status |
|------|-----------|--------|
| slj (GenAI SDK) | dr4 (Gemini provider) | Unblocked when dr4 completes |
| iq5 (creative_story) | dr4 (Gemini) + Neo APIs | Cross-project dependency |
| s3i (DB migration) | iq5 | Needs run type defined first |
| gcr (narration) | iq5 | Needs storyboard pipeline |
| wv3 (interleaved stream) | iq5 | Needs run type |
| 6yb (video stitch) | gcr (narration) | Needs audio first |
| egu (GCP deploy) | iq5 | Needs working pipeline |
| jh1 (arch diagram) | egu | Needs deployment defined |
| dwn (README) | egu | Needs deployment |
| 64f (templates) | nf2 (mode selector) | Needs mode UI |
| 21f (Docker Compose) | nf2 | Needs mode selector |
| 0ov (compare view) | 21y (consent UX) | Needs consent flow |
| www (credits) | nf2 (mode selector) | Post-submission |
| ukf (team workspace) | www (credits) | Post-submission |

### Ready to Start Now (no blockers)
| Bead | Priority | Description |
|------|----------|-------------|
| **dr4** | P0 | Add Gemini provider to LLM router |
| **nf2** | P1 | Add mode selector: Story Director vs Historical Lens |
| **0qn** | P2 | Add export-ready trust card |
| **21y** | P2 | Add safety consent UX |
| **1b9** | P2 | Add client analytics instrumentation |

---

## neo-mumbai-noir (3 beads)

### By Priority
| Priority | Count | IDs |
|----------|-------|-----|
| P1 | 3 | rft, qc1, n77 |

### All Tasks
| Bead | Type | Description | Blocked By |
|------|------|-------------|-----------|
| **rft** | feature | Expose character extraction as API service | None — **ready now** |
| qc1 | feature | Expose image search as API service | rft |
| n77 | feature | Expose storyboard assembly as API service | rft |

### Ready to Start Now
| Bead | Priority | Description |
|------|----------|-------------|
| **rft** | P1 | Expose character extraction as API service |

---

## Recommended Sprint Plan

### Sprint 1 (Week 1): Foundation
**Start in parallel:**
- chrono-canvas: **dr4** (Gemini provider) + **nf2** (mode selector)
- neo-mumbai-noir: **rft** (extraction API)

### Sprint 2 (Week 2): Core Pipeline
- chrono-canvas: **slj** (GenAI SDK), **iq5** (creative_story), **21f** (Docker Compose)
- neo-mumbai-noir: **qc1** (search API), **n77** (storyboard API)

### Sprint 3 (Week 3): Multimodal + Integration
- chrono-canvas: **s3i** (DB migration), **gcr** (narration), **wv3** (interleaved stream), **egu** (GCP)

### Sprint 4 (Week 4): Polish + Submission Prep
- chrono-canvas: **6yb** (video stitch), **jh1** (diagram + demo), **dwn** (README)

### Sprint 5 (Week 5): Trust Layer
- chrono-canvas: **0qn** (trust card), **21y** (consent), **0ov** (compare view), **64f** (templates), **1b9** (analytics)

### Sprint 6+ (Post-submission): Monetization
- chrono-canvas: **www** (credits), **ukf** (team workspace)

---

## Summary

| Project | Total | P0 | P1 | P2 | P3 | Ready Now | Blocked |
|---------|-------|----|----|----|----|-----------|---------|
| chrono-canvas | 19 | 2 | 10 | 5 | 2 | 5 | 14 |
| neo-mumbai-noir | 3 | 0 | 3 | 0 | 0 | 1 | 2 |
| **Total** | **22** | **2** | **13** | **5** | **2** | **6** | **16** |
