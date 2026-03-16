"""Generate noir title cards and tech showcase cards using Pillow."""
import sys
import textwrap
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

W, H = 1920, 1080


def _load_fonts(title_size=64, body_size=28, code_size=22):
    mono_paths = [
        "/System/Library/Fonts/Menlo.ttc",
        "/System/Library/Fonts/Courier.dfont",
        "/Library/Fonts/Courier New.ttf",
    ]
    title_font = body_font = code_font = None
    for p in mono_paths:
        try:
            title_font = ImageFont.truetype(p, title_size)
            body_font = ImageFont.truetype(p, body_size)
            code_font = ImageFont.truetype(p, code_size)
            break
        except (OSError, IOError):
            continue
    if title_font is None:
        title_font = body_font = code_font = ImageFont.load_default()
    return title_font, body_font, code_font


def make_card(title: str, subtitle: str, out_path: str, title_size: int = 64):
    img = Image.new("RGB", (W, H), "black")
    draw = ImageDraw.Draw(img)
    title_font, body_font, _ = _load_fonts(title_size=title_size)

    bbox = draw.textbbox((0, 0), title, font=title_font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    tx = (W - tw) // 2
    ty = (H - th) // 2 - 40
    draw.text((tx, ty), title, fill="white", font=title_font)

    if subtitle:
        bbox2 = draw.textbbox((0, 0), subtitle, font=body_font)
        sw = bbox2[2] - bbox2[0]
        sx = (W - sw) // 2
        sy = ty + th + 30
        draw.text((sx, sy), subtitle, fill="#888888", font=body_font)

    img.save(out_path)


def make_code_card(title: str, code: str, out_path: str, accent: str = "#4EC9B0"):
    """Card with title + syntax-highlighted-ish code block."""
    img = Image.new("RGB", (W, H), "#0d0d0d")
    draw = ImageDraw.Draw(img)
    title_font, _, code_font = _load_fonts(title_size=36, code_size=20)

    # Title bar
    draw.rectangle([(0, 0), (W, 60)], fill="#1a1a1a")
    draw.text((40, 14), title, fill=accent, font=title_font)

    # Code block
    y = 90
    line_height = 28
    for line in code.split("\n"):
        if not line.strip():
            y += line_height // 2
            continue
        # Simple coloring: comments gray, strings green, keywords blue
        color = "#d4d4d4"  # default
        stripped = line.strip()
        if stripped.startswith("#") or stripped.startswith("//"):
            color = "#6A9955"
        elif "def " in line or "async " in line or "await " in line or "for " in line or "if " in line or "while " in line or "return " in line or "class " in line:
            color = "#569CD6"
        elif '"""' in line or "'''" in line:
            color = "#CE9178"
        elif "yield " in line:
            color = "#C586C0"

        draw.text((40, y), line, fill=color, font=code_font)
        y += line_height
        if y > H - 40:
            break

    img.save(out_path)


def make_arch_card(out_path: str):
    """Architecture overview card."""
    img = Image.new("RGB", (W, H), "#0d0d0d")
    draw = ImageDraw.Draw(img)
    title_font, body_font, code_font = _load_fonts(title_size=40, body_size=24, code_size=20)

    draw.text((W // 2 - 200, 40), "ARCHITECTURE", fill="white", font=title_font)

    # Draw boxes
    boxes = [
        # (x, y, w, h, label, sublabel, color)
        (120, 160, 300, 80, "Next.js Frontend", "React + TypeScript", "#3178C6"),
        (120, 300, 300, 80, "FastAPI Backend", "Python async", "#009688"),
        (560, 160, 340, 80, "Gemini 2.5 Flash", "Text + Interleaved", "#4285F4"),
        (560, 300, 340, 80, "Gemini 3.1 Flash", "Image Generation", "#EA4335"),
        (560, 440, 340, 80, "Gemini Live API", "Native Audio (Charon)", "#FBBC04"),
        (1040, 160, 300, 80, "Imagen 4 Fast", "Fallback Image Gen", "#34A853"),
        (1040, 300, 300, 80, "Veo 3.1 / 3.0", "Video Generation", "#EA4335"),
        (1040, 440, 300, 80, "Cloud Run", "Deployed", "#4285F4"),
        (120, 440, 300, 80, "WebSocket Proxy", "Bidirectional Audio", "#FF6F00"),
    ]

    for bx, by, bw, bh, label, sub, color in boxes:
        draw.rectangle([(bx, by), (bx + bw, by + bh)], outline=color, width=2)
        draw.text((bx + 12, by + 12), label, fill="white", font=code_font)
        draw.text((bx + 12, by + 40), sub, fill="#888888", font=code_font)

    # Arrows (simple lines)
    arrow_color = "#555555"
    # Frontend → Backend
    draw.line([(270, 240), (270, 300)], fill=arrow_color, width=2)
    # Backend → Models
    draw.line([(420, 200), (560, 200)], fill=arrow_color, width=2)
    draw.line([(420, 340), (560, 340)], fill=arrow_color, width=2)
    draw.line([(420, 480), (560, 480)], fill=arrow_color, width=2)
    # Models → Fallbacks
    draw.line([(900, 200), (1040, 200)], fill=arrow_color, width=2)
    draw.line([(900, 340), (1040, 340)], fill=arrow_color, width=2)
    draw.line([(900, 480), (1040, 480)], fill=arrow_color, width=2)

    # Open source callout
    draw.text((120, 580), "github.com/anthropics — Open Source", fill="#888888", font=body_font)
    draw.text((120, 620), "Built for Google Gemini API Developer Competition", fill="#555555", font=body_font)

    img.save(out_path)


def make_stack_card(out_path: str):
    """Tech stack summary card."""
    img = Image.new("RGB", (W, H), "#0d0d0d")
    draw = ImageDraw.Draw(img)
    title_font, body_font, _ = _load_fonts(title_size=40, body_size=26)

    draw.text((W // 2 - 150, 50), "TECH STACK", fill="white", font=title_font)

    items = [
        ("MODELS", [
            "Gemini 2.5 Flash — story text, scene narration",
            "Gemini 3.1 Flash — interleaved text+image",
            "Gemini Live API — native audio (Charon voice)",
            "Imagen 4 Fast — fallback image generation",
            "Veo 3.1 / 3.0 — video generation",
        ]),
        ("STACK", [
            "FastAPI + async Python backend",
            "Next.js + React + TypeScript frontend",
            "Google GenAI SDK (google-genai)",
            "Cloud Run — containerized deployment",
        ]),
    ]

    y = 140
    for section, lines in items:
        draw.text((120, y), section, fill="#4EC9B0", font=body_font)
        y += 45
        for line in lines:
            draw.text((160, y), f"  {line}", fill="#cccccc", font=body_font)
            y += 38
        y += 20

    img.save(out_path)


if __name__ == "__main__":
    out_dir = Path(sys.argv[1])
    out_dir.mkdir(parents=True, exist_ok=True)

    # Title cards
    cards = [
        ("C H R O N O C A N V A S", "Walk in with a whisper. Walk out with a film.", "title.png", 60),
        ("LIVE STORY", "Interleaved text + image generation", "card-livestory.png", 52),
        ("LIVE SESSION", "Voice conversation with Dash", "card-livesession.png", 52),
        ("STORY DIRECTOR", "Full pipeline audit trail", "card-storydirector.png", 52),
        ("UNDER THE HOOD", "Open source  —  github.com", "card-tech.png", 52),
        ("Music: Surprising Media", "pixabay.com/users/surprising_media-11873433", "card-credits.png", 40),
    ]
    for title, sub, filename, size in cards:
        make_card(title, sub, str(out_dir / filename), size)
        print(f"  ✓ {filename}")

    # Architecture card
    make_arch_card(str(out_dir / "tech-architecture.png"))
    print("  ✓ tech-architecture.png")

    # Stack card
    make_stack_card(str(out_dir / "tech-stack.png"))
    print("  ✓ tech-stack.png")

    # Code cards
    make_code_card(
        "live_story.py — Interleaved Streaming",
        '''\
# Real-time streaming: text and images arrive together
for part in chunk.candidates[0].content.parts:
    if part.text is not None:
        accumulated_text.append(part.text)

    elif part.inline_data is not None:
        # Flush pending text BEFORE the image
        if accumulated_text and not text_yielded:
            clean = strip_markdown(joined)
            yield {"type": "text", "content": clean}
            text_yielded = True

        # Stream the image immediately
        b64 = base64.b64encode(part.inline_data.data)
        yield {"type": "image", "content": b64}''',
        str(out_dir / "tech-code-streaming.png"),
    )
    print("  ✓ tech-code-streaming.png")

    make_code_card(
        "live_story.py — Character Consistency Protocol",
        '''\
DASH_SYSTEM_INSTRUCTION = """
CHARACTER CONSISTENCY (CRITICAL):
Before telling the story, mentally cast your characters.
Lock in each character's exact physical appearance:
  face shape, skin tone, hair color/style, eye color,
  build, age, distinguishing marks, and wardrobe.

Once set, NEVER deviate. Every image must depict the
SAME person with IDENTICAL features.

When generating images, ALWAYS re-state each visible
character's key physical features in your internal
image description — do NOT rely on context alone.
"""''',
        str(out_dir / "tech-code-character.png"),
        accent="#CE9178",
    )
    print("  ✓ tech-code-character.png")

    make_code_card(
        "live_session.py — Gemini Live API Voice Bridge",
        '''\
def _build_live_config(voice_name="Charon"):
    return types.LiveConnectConfig(
        response_modalities=["AUDIO"],
        system_instruction=SYSTEM_INSTRUCTION,
        speech_config=types.SpeechConfig(
            voice_config=types.VoiceConfig(
                prebuilt_voice_config=types.PrebuiltVoiceConfig(
                    voice_name=voice_name
                )
            )
        ),
        tools=LIVE_TOOLS,
    )

# Multi-turn receive — re-call receive() each turn
while not stop_event.is_set():
    aiter = session.receive().__aiter__()
    while not stop_event.is_set():
        response = await asyncio.wait_for(
            aiter.__anext__(), timeout=120
        )''',
        str(out_dir / "tech-code-voice.png"),
        accent="#FBBC04",
    )
    print("  ✓ tech-code-voice.png")

    make_code_card(
        "live_story.py — Multi-Model Fallback Chain",
        '''\
_MODEL_CHAIN = [
    "gemini-3.1-flash-image-preview",  # primary
    "gemini-2.5-flash-image",           # fallback
]
_IMAGE_FALLBACK_CHAIN = [
    "gemini-2.5-flash-image",
    "imagen-4.0-fast-generate-001",     # fastest, no refs
]

for img_model in image_models_to_try:
    is_imagen = img_model.startswith("imagen")
    is_3x = img_model.startswith("gemini-3")

    if is_imagen:
        # Imagen: fastest (~2s), no reference images
        response = await client.aio.models.generate_images(...)
    elif is_3x:
        # 3.x: input images suppress output images
        contents = image_prompt_text
    else:
        # 2.5: pass casting portrait for consistency
        if ref_img:
            parts.append(types.Part.from_bytes(
                data=ref_img, mime_type=ref_mime
            ))''',
        str(out_dir / "tech-code-fallback.png"),
        accent="#34A853",
    )
    print("  ✓ tech-code-fallback.png")
