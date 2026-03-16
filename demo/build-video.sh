#!/usr/bin/env bash
set -euo pipefail

# ─────────────────────────────────────────────
# ChronoCanvas Hackathon Demo — 4min Video
# ─────────────────────────────────────────────

DIR="$(cd "$(dirname "$0")" && pwd)"
ASSETS="$DIR/assets"
TMP="$DIR/.tmp"
OUT="$DIR/chrononoir-demo.mp4"

W=1920; H=1080; FPS=30

rm -rf "$TMP"
mkdir -p "$TMP"

# ── 1. Generate all cards ──
echo "▸ Generating cards..."
python3 "$DIR/make_cards.py" "$TMP"

# ── 2. Scale screenshots ──
echo "▸ Preparing screenshots..."
scale_img() {
  ffmpeg -y -i "$1" \
    -vf "scale=${W}:${H}:force_original_aspect_ratio=decrease,pad=${W}:${H}:(ow-iw)/2:(oh-ih)/2:black,format=yuv420p" \
    "$2" 2>/dev/null
}

scale_img "$ASSETS/Live-Story-prompt-entry.png"       "$TMP/ls-01.png"
scale_img "$ASSETS/Live-Story-casting.png"             "$TMP/ls-02.png"
scale_img "$ASSETS/Live-Story-Scene-1.png"             "$TMP/ls-03.png"
scale_img "$ASSETS/Live-Story-Scene2-Mid-sentence.png" "$TMP/ls-04.png"
scale_img "$ASSETS/Live-Session-Speaking-into-mic.png" "$TMP/sn-01.png"
scale_img "$ASSETS/Live-Session-setup.png"             "$TMP/sn-02.png"
scale_img "$ASSETS/Live-Session-Scene-1.png"           "$TMP/sn-03.png"

# ── 3. Create clips ──
echo "▸ Creating clips..."

# Ken Burns: slow zoom
still() {
  local img="$1" out="$2" dur="$3"
  ffmpeg -y -loop 1 -i "$img" -t "$dur" \
    -vf "zoompan=z='1+0.0008*on':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=$((dur * FPS)):s=${W}x${H}:fps=${FPS},fade=t=in:d=0.4,fade=t=out:st=$(echo "$dur - 0.4" | bc):d=0.4,format=yuv420p" \
    -c:v libx264 -pix_fmt yuv420p "$out" 2>/dev/null
}

# Static card
card() {
  local img="$1" out="$2" dur="$3"
  ffmpeg -y -loop 1 -i "$img" -t "$dur" \
    -vf "scale=${W}:${H},fade=t=in:d=0.5,fade=t=out:st=$(echo "$dur - 0.5" | bc):d=0.5,format=yuv420p" \
    -r $FPS -c:v libx264 -pix_fmt yuv420p "$out" 2>/dev/null
}

# Crop + trim recording (remove toolbar, trim last 3s)
crop_rec() {
  local src="$1" out="$2"
  local full_dur
  full_dur=$(ffprobe -v quiet -show_entries format=duration -of csv=p=0 "$src")
  local trim_dur
  trim_dur=$(echo "$full_dur - 3" | bc)
  local fade_at
  fade_at=$(echo "$trim_dur - 0.8" | bc)
  ffmpeg -y -i "$src" -t "$trim_dur" \
    -vf "crop=in_w:in_h-120:0:50,scale=${W}:${H},fade=t=in:d=0.4,fade=t=out:st=${fade_at}:d=0.8,format=yuv420p" \
    -c:v libx264 -pix_fmt yuv420p -r $FPS "$out" 2>/dev/null
}

# Clip index
N=0
clip() { printf -v CLIP "v%02d" $N; N=$((N + 1)); }

# ═══════════════════════════════════════
# SECTION 1: Title (5s)
# ═══════════════════════════════════════
clip; card "$TMP/title.png" "$TMP/$CLIP.mp4" 5

# ═══════════════════════════════════════
# SECTION 2: Live Story (~80s)
# ═══════════════════════════════════════
clip; card "$TMP/card-livestory.png" "$TMP/$CLIP.mp4" 3

# Screenshots: prompt → casting → scenes
clip; still "$TMP/ls-01.png" "$TMP/$CLIP.mp4" 4
clip; still "$TMP/ls-02.png" "$TMP/$CLIP.mp4" 5
clip; still "$TMP/ls-03.png" "$TMP/$CLIP.mp4" 4
clip; still "$TMP/ls-04.png" "$TMP/$CLIP.mp4" 4

# Screen recording
echo "▸ Processing Live Story recording..."
clip; crop_rec "$ASSETS/rec-live-story.mov" "$TMP/$CLIP.mp4"

# ═══════════════════════════════════════
# SECTION 3: Live Session (~50s)
# ═══════════════════════════════════════
clip; card "$TMP/card-livesession.png" "$TMP/$CLIP.mp4" 3

# Screenshots
clip; still "$TMP/sn-01.png" "$TMP/$CLIP.mp4" 4
clip; still "$TMP/sn-02.png" "$TMP/$CLIP.mp4" 5
clip; still "$TMP/sn-03.png" "$TMP/$CLIP.mp4" 4

# Screen recording
echo "▸ Processing Live Session recording..."
clip; crop_rec "$ASSETS/rec-live-session.mov" "$TMP/$CLIP.mp4"

# ═══════════════════════════════════════
# SECTION 4: Story Director (~17s)
# ═══════════════════════════════════════
clip; card "$TMP/card-storydirector.png" "$TMP/$CLIP.mp4" 2.5

echo "▸ Processing Story Director recording..."
clip; crop_rec "$ASSETS/Story-Director-audit.mov" "$TMP/$CLIP.mp4"

echo "▸ Processing audit screen recording..."
# Use ~36s of the longer audit recording (trim last 3s for toolbar, cap at 36s)
clip
AUDIT_FULL=$(ffprobe -v quiet -show_entries format=duration -of csv=p=0 "$ASSETS/rec-audit.mov")
AUDIT_DUR=$(echo "if ($AUDIT_FULL - 3 > 36) 36 else $AUDIT_FULL - 3" | bc)
AUDIT_FADE=$(echo "$AUDIT_DUR - 0.8" | bc)
ffmpeg -y -i "$ASSETS/rec-audit.mov" -t "$AUDIT_DUR" \
  -vf "crop=in_w:in_h-120:0:50,scale=${W}:${H},fade=t=in:d=0.4,fade=t=out:st=${AUDIT_FADE}:d=0.8,format=yuv420p" \
  -c:v libx264 -pix_fmt yuv420p -r $FPS "$TMP/$CLIP.mp4" 2>/dev/null

# ═══════════════════════════════════════
# SECTION 5: Technical Deep Dive (~60s)
# ═══════════════════════════════════════
clip; card "$TMP/card-tech.png" "$TMP/$CLIP.mp4" 3

# Architecture + stack
clip; still "$TMP/tech-architecture.png" "$TMP/$CLIP.mp4" 8
clip; still "$TMP/tech-stack.png" "$TMP/$CLIP.mp4" 8

# Code cards
clip; still "$TMP/tech-code-streaming.png" "$TMP/$CLIP.mp4" 10
clip; still "$TMP/tech-code-character.png" "$TMP/$CLIP.mp4" 8
clip; still "$TMP/tech-code-voice.png" "$TMP/$CLIP.mp4" 10
clip; still "$TMP/tech-code-fallback.png" "$TMP/$CLIP.mp4" 10

# ═══════════════════════════════════════
# SECTION 6: Credits (3s)
# ═══════════════════════════════════════
clip; card "$TMP/card-credits.png" "$TMP/$CLIP.mp4" 3

# ── 4. Concatenate ──
echo "▸ Concatenating $N clips..."
> "$TMP/concat.txt"
for i in $(seq 0 $((N - 1))); do
  printf "file 'v%02d.mp4'\n" "$i" >> "$TMP/concat.txt"
done

ffmpeg -y -f concat -safe 0 -i "$TMP/concat.txt" \
  -c:v libx264 -pix_fmt yuv420p "$TMP/video.mp4" 2>/dev/null

# ── 5. Add music ──
echo "▸ Adding music..."
TOTAL=$(ffprobe -v quiet -show_entries format=duration -of csv=p=0 "$TMP/video.mp4")
FADE_AT=$(echo "$TOTAL - 3" | bc)
MUSIC="$ASSETS/surprising_media-dancing-saxophone-dark-jazz-388468.mp3"

ffmpeg -y \
  -i "$TMP/video.mp4" \
  -i "$MUSIC" \
  -filter_complex "[1:a]afade=t=in:d=2,afade=t=out:st=${FADE_AT}:d=3,volume=0.3[a]" \
  -map 0:v -map "[a]" \
  -c:v copy -c:a aac -shortest \
  "$OUT" 2>/dev/null

# ── 6. Done ──
rm -rf "$TMP"
FINAL=$(ffprobe -v quiet -show_entries format=duration -of csv=p=0 "$OUT")
MINS=$(echo "$FINAL / 60" | bc)
SECS=$(echo "$FINAL - ($MINS * 60)" | bc | xargs printf '%.0f')
echo ""
echo "✓ Done: $OUT"
echo "  Duration: ${MINS}m ${SECS}s"
echo "  Resolution: ${W}x${H}"
