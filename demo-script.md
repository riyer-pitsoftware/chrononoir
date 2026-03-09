# ChronoCanvas Demo Script — Hackathon Screen Recording

**Target duration:** 3:00–3:30
**Track:** Creative Storyteller
**Rule:** Show the product, not the plumbing. No architecture slides. No apologies.

---

## Pre-Recording Checklist

- [ ] Docker services running: `docker compose ps` — db, redis, api, worker, frontend all healthy
- [ ] Smoke test passes: `docker exec chrono-canvas-api-1 python /app/scripts/smoke_test.py`
- [ ] `HACKATHON_MODE=true` in `.env` (Story Director default, clean sidebar)
- [ ] Browser: Chrome, 1920x1080, incognito, no extensions, bookmark bar hidden
- [ ] Microphone tested and working (for voice input segment)
- [ ] Clear any previous generation requests so the UI is clean
- [ ] Screen recorder configured: OBS or QuickTime, system audio + mic, 1080p 30fps
- [ ] Close all notifications, Slack, email — nothing pops up mid-recording
- [ ] Do one full dry run end-to-end to warm caches and verify timing

---

## The Story Prompt

**Voice version (speak this):**
> "A jazz musician in 1940s New Orleans discovers a photograph in a pawnshop — a photograph of himself, taken thirty years before he was born."

**Text version (for interleaved segment):**
> "A woman in a rain-soaked trench coat stands outside a shuttered jazz club on Bourbon Street. The neon sign flickers. She's holding an envelope she hasn't opened yet."

---

## Script

### Segment 1 — Voice Prompt (0:00–0:30)

**Action:** Open ChronoNoir Studio. The Story Director page loads.

**Click:** Microphone icon in the prompt area.

**Speak:** _"A jazz musician in 1940s New Orleans discovers a photograph in a pawnshop — a photograph of himself, taken thirty years before he was born."_

**Expected:** LiveVoicePrompt component shows transcript, then Dash responds with a noir-flavored expansion — something like _"Now that's a setup. A man walks into a pawnshop and finds his own ghost staring back from behind cracked glass..."_

**Click:** "Use This" button to accept Dash's expanded prompt.

**Voiceover note:** No narration needed here — let the voice interaction speak for itself. The audience should see a human speak and an AI creative director respond.

**Fallback:** If mic doesn't register, type the prompt directly. Skip to pipeline. Lose 15 seconds, but don't fumble.

---

### Segment 2 — Pipeline Streams (0:30–1:30)

**Action:** Generation begins automatically after "Use This." The pipeline progress area shows nodes activating in sequence.

**Expected on screen:**
- `story_orchestrator` → `character_extraction` → `scene_decomposition` (5-8 seconds)
- Scene count appears (expect 4-6 scenes)
- `scene_prompt_generation` runs in parallel — prompts stream in
- `prompt_validation` scores and optionally repairs prompts
- `scene_image_generation` — **this is the money shot**: images appear one by one as they generate. Each panel populates with a noir-lit Imagen 4 illustration.
- `storyboard_coherence` — brief pause as Gemini reviews all panels together

**Voiceover note (if recording with audio):** _"Each scene is decomposed, prompted, illustrated, and reviewed — all streaming live to the browser."_ Keep it to one sentence. Let the visuals carry.

**Timing:** This segment runs ~45-60 seconds depending on Imagen speed. If it's faster, let the silence build — watching images appear is compelling.

**Fallback:** If one panel fails (Imagen filter), the pipeline continues with remaining panels. Don't mention it. If the whole pipeline stalls past 90 seconds, cut and re-record.

---

### Segment 3 — Storyboard Reveal + Voice Narration (1:30–2:00)

**Action:** Pipeline completes. Full storyboard is visible with all panels, narration text beneath each.

**Pause:** Let the storyboard breathe for 3-4 seconds. The audience needs a moment to take it in.

**Click:** Speaker icon on the most visually striking panel (probably scene 2 or 3).

**Expected:** Dash's voice narrates the panel via Gemini Live API. The narration should reference specific visual elements in the image (vision-enhanced narration).

**Voiceover note:** Silence during playback. Let Dash's voice fill the space.

**Fallback:** If Live API narration is slow to start (>3 seconds), click the TTS-generated audio instead (pre-rendered during pipeline). Both produce narration; Live API is more impressive but TTS is more reliable.

---

### Segment 4 — Interleaved Text+Image (2:00–2:45)

**Action:** Navigate to the LiveStory page (sidebar or direct link).

**Type the text prompt:** _"A woman in a rain-soaked trench coat stands outside a shuttered jazz club on Bourbon Street. The neon sign flickers. She's holding an envelope she hasn't opened yet."_

**Click:** Generate / Submit.

**Expected:** A single Gemini 2.0 Flash response streams interleaved content — text paragraphs and inline images arriving together in sequence. The page renders them as they arrive: a paragraph of noir prose, then an image, then more prose, then another image.

**Voiceover note:** _"This is interleaved output — Gemini generates text and images in a single response, not as separate calls. The story and the visuals arrive together."_ One sentence of context, then let it stream.

**This is the mandatory track feature.** Give it 30-40 seconds of screen time. Don't rush past it.

**Fallback:** If the stream is slow, wait. Partial output is still impressive. If it fails completely, skip to segment 5 — the main storyboard pipeline already demonstrated the core value.

---

### Segment 5 — Conversational Refinement (2:45–3:15)

**Action:** Navigate back to the storyboard from Segment 2.

**Open chat/refinement panel.**

**Type:** _"Make scene 3 darker — more shadow, less color. Like the lights just went out."_

**Expected:** Gemini reads the instruction with the actual panel images as context, suggests an edit, and regenerates the scene. The panel updates in place.

**Voiceover note:** _"The AI sees the images it created. It's not just editing a prompt — it's looking at its own work and deciding what to change."_

**Fallback:** If regeneration is slow, show the suggestion text (which arrives quickly) and cut before the image finishes. The conversational understanding is the point, not the regen speed.

---

### Segment 6 — Export + Close (3:15–3:30)

**Action:** Click export/download. Show the video player with the assembled MP4 (Ken Burns effect, crossfade transitions, narration audio).

**Play 3-5 seconds** of the exported video. Just enough to prove it's real.

**Quick cut to:** Audit trail page. Show 2-3 rows of LLM calls with provider, tokens, cost, duration. **Do not linger.** This is for Judge Ravi (technical), not Sofia (demo).

**End card:** Fade to black or show the ChronoNoir Studio logo. No "thanks for watching." Let it end like a film.

---

## Timing Budget

| Segment | Target | Buffer |
|---------|--------|--------|
| Voice prompt | 0:30 | Can compress to 0:20 if voice is fast |
| Pipeline streams | 1:00 | May run 0:45–1:15 depending on Imagen |
| Storyboard + narration | 0:30 | Fixed — just reveal and play |
| Interleaved output | 0:45 | **Don't compress** — mandatory feature |
| Refinement | 0:30 | Can skip if over time |
| Export + close | 0:15 | Cut audit trail if tight |
| **Total** | **3:30** | **Floor: 2:45, ceiling: 3:45** |

---

## Recording Notes

- **One take if possible.** Cuts between segments are OK but seamless flow is better.
- **Mouse movements:** Slow and deliberate. No frantic clicking. A director doesn't rush.
- **If something fails mid-recording:** Don't react. Don't say "oops." Cut, fix, re-record that segment. Splice in post.
- **Audio:** System audio (for TTS/narration playback) + mic (for voice prompt + optional voiceover). Balance so Dash's voice is louder than yours.
- **Browser zoom:** 100%. Font should be legible at 1080p without squinting.
