#!/usr/bin/env python3
"""
Generate 34 portrait-format reel frames using DALL-E 3.
Each image: consistent characters + dialogue text overlay.
"""

import os
import io
import time
import textwrap
import requests
from openai import OpenAI
from PIL import Image, ImageDraw, ImageFont

API_KEY = os.environ.get("OPENAI_API_KEY", "")
IMAGE_MODEL = "gpt-image-1"
IMAGE_SIZE  = "1024x1536"
OUTPUT_DIR  = "portrait_frames"
FONT_BOLD   = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
FONT_REG    = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"

os.makedirs(OUTPUT_DIR, exist_ok=True)
client = OpenAI(api_key=API_KEY)

# ── Character & setting descriptions (kept identical across all prompts) ──────
CUSTOMER_DESC = (
    "a young Indian boy about 12 years old with short black hair, wearing a blue t-shirt, "
    "cute expressive face, big bright eyes, 3D Pixar animated style"
)
SHOPKEEPER_DESC = (
    "an Indian adult man about 30 years old with a neatly trimmed short black beard, "
    "wearing a dark black polo shirt, friendly handsome face, 3D Pixar animated style"
)
SETTING = (
    "inside a warm well-lit Indian clothing store, wooden shelves stacked with colourful "
    "neatly folded t-shirts in the background, NO sarees, only t-shirts visible, "
    "realistic 3D Pixar render, cinematic portrait"
)

# ── Scene list: (frame_number, speaker, dialogue_text, emotion/action_hint) ──
SCENES = [
    ( 1,  "Customer",    "Arey ye T-shirt\nkitne ka hai?",
      "pointing at a green t-shirt hanging on a hanger, curious excited expression"),
    ( 2,  "Shopkeeper",  "500 ka hai.",
      "standing behind counter, calm confident expression, one hand raised"),
    ( 3,  "Customer",    "Aisa 10 T-shirt\nlega tere se.\nPar ek shirt hai.",
      "smiling slyly, arms crossed, clever expression"),
    ( 4,  "Shopkeeper",  "Kya?",
      "confused surprised expression, eyebrow raised, leaning forward"),
    ( 5,  "Customer",    "Kuch savaal puchega\ntere se. Phir sahaab\ndena ka hai tere ko.",
      "holding up one finger, explaining something, determined look"),
    ( 6,  "Shopkeeper",  "Theek hai.",
      "nodding with a relaxed agreeable smile"),
    ( 7,  "Customer",    "Naam kya hai tera?",
      "smiling innocently, hands clasped"),
    ( 8,  "Shopkeeper",  "Pavan.",
      "smiling proudly, hand on chest"),
    ( 9,  "Customer",    "Kidhar rehta hai?",
      "tilting head curiously, inquisitive expression"),
    (10,  "Shopkeeper",  "Ghar pe.",
      "amused smirk, casual shrug"),
    (11,  "Customer",    "Do ke baad kya\naata hai?",
      "thinking pose with finger on chin, mischievous grin"),
    (12,  "Shopkeeper",  "Teen.",
      "simple calm answer, holding up 3 fingers"),
    (13,  "Customer",    "Maine kaunse color\nka shirt pehna hai?",
      "pointing to his own blue t-shirt, grinning proudly"),
    (14,  "Shopkeeper",  "Blue.",
      "pointing at the boy with a knowing smile"),
    (15,  "Customer",    "Shaadi ho\ngaya hai tera?",
      "smiling cheekily, raising eyebrows"),
    (16,  "Shopkeeper",  "Nahi.",
      "shaking head, slightly embarrassed smile"),
    (17,  "Customer",    "Kitne bacche hain?",
      "asking with a straight face, arms folded"),
    (18,  "Shopkeeper",  "Teen.",
      "confused look, scratching head, realising the trick"),
    (19,  "Customer",    "Saturday ke baad\nkya aata hai?",
      "holding up index finger with a clever smirk"),
    (20,  "Shopkeeper",  "Sunday.",
      "answering simply, calm smile"),
    (21,  "Customer",    "Right ka opposite\nkya hota hai?",
      "pointing sideways, curious expression"),
    (22,  "Shopkeeper",  "Left.",
      "pointing left with a chuckle"),
    (23,  "Customer",    "T-shirt kitne\nka hai?",
      "pointing at a t-shirt on the shelf, smiling"),
    (24,  "Shopkeeper",  "500 ka.",
      "showing five fingers, confident"),
    (25,  "Customer",    "Tere ko kitne\npadaa?",
      "leaning in with a tricky grin"),
    (26,  "Shopkeeper",  "50 me.",
      "holding up two fingers with a proud grin, realising something is off"),
    (27,  "Customer",    "Kya karne ka hai\nabhi bata? Cheating\nhai ye. Hehe.",
      "laughing and pointing, arms crossed, very amused"),
    (28,  "Shopkeeper",  "70 rupaye me dega\nmain aapko.",
      "leaning forward with a negotiating smile, hands out"),
    (29,  "Customer",    "Tu free me\ndega mere ko.",
      "smiling confidently, arms crossed, very sure of himself"),
    (30,  "Shopkeeper",  "Kaay ko?",
      "confused disbelieving expression, hands up"),
    (31,  "Customer",    "Ae dekho, ye 50 ka\nT-shirt 500 me...",
      "holding up the green t-shirt, smiling triumphantly"),
    (32,  "Shopkeeper",  "Arey hehe... mazak\nkar rahe hain bhaiya.\nLeke jao free me.",
      "laughing loudly with both hands raised, generous expression"),
    (33,  "Customer",    "Thank you! Aur naya\nmaal aaye toh bata.",
      "waving thank you, walking away happily with the t-shirt"),
    (34,  "Shopkeeper",  "Main ja raha hoon\nye shehar chhod ke.",
      "looking defeated and sad, head in hands, dramatic expression"),
]

CLOSING = {
    "num": 35,
    "prompt": (
        f"Cinematic closing shot portrait 9:16. {CUSTOMER_DESC} walking out of a "
        f"clothing store door into bright daylight, carrying a bag with t-shirts, "
        f"back to camera, triumphant pose. {SETTING}. No text."
    ),
    "filename": "scene_35_closing.png",
}


# ── Build DALL-E prompt ───────────────────────────────────────────────────────
def build_prompt(speaker: str, emotion: str) -> str:
    if speaker == "Customer":
        char = CUSTOMER_DESC
    else:
        char = SHOPKEEPER_DESC
    return (
        f"Vertical portrait 9:16 cinematic illustration. {char}, {emotion}. "
        f"{SETTING}. Vibrant colours, sharp details, no text, no watermark."
    )


# ── Add text overlay ──────────────────────────────────────────────────────────
CUSTOMER_COLOR   = (220, 30, 30)   # red
SHOPKEEPER_COLOR = (180, 90, 0)    # dark orange
TEXT_BG          = (255, 255, 255, 210)  # semi-transparent white

def add_text_overlay(img: Image.Image, scene_num: int, speaker: str, dialogue: str) -> Image.Image:
    img = img.convert("RGBA")
    w, h = img.size

    banner_h = int(h * 0.22)
    overlay = Image.new("RGBA", (w, banner_h), TEXT_BG)
    img.paste(overlay, (0, 0), overlay)

    draw = ImageDraw.Draw(img)

    # Badge
    badge_r = int(w * 0.07)
    bx, by = int(w * 0.05), int(h * 0.015)
    draw.ellipse([bx, by, bx + badge_r*2, by + badge_r*2],
                 fill=(220, 30, 30))
    try:
        badge_font = ImageFont.truetype(FONT_BOLD, int(badge_r * 1.1))
    except Exception:
        badge_font = ImageFont.load_default()
    draw.text((bx + badge_r, by + badge_r), str(scene_num),
              font=badge_font, fill="white", anchor="mm")

    # Speaker name
    try:
        spk_font = ImageFont.truetype(FONT_BOLD, int(w * 0.065))
    except Exception:
        spk_font = ImageFont.load_default()

    color = CUSTOMER_COLOR if speaker == "Customer" else SHOPKEEPER_COLOR
    spk_x = bx + badge_r*2 + int(w * 0.04)
    spk_y = int(banner_h * 0.10)
    draw.text((spk_x, spk_y), f"{speaker}:", font=spk_font, fill=color)

    # Dialogue text
    try:
        dlg_font = ImageFont.truetype(FONT_BOLD, int(w * 0.058))
    except Exception:
        dlg_font = ImageFont.load_default()

    dlg_y = spk_y + int(w * 0.075)
    margin = int(w * 0.05)
    max_chars = 22
    lines = []
    for raw_line in dialogue.split("\n"):
        lines.extend(textwrap.wrap(raw_line, max_chars) or [""])

    for line in lines:
        draw.text((margin, dlg_y), line, font=dlg_font, fill=(20, 20, 20))
        dlg_y += int(w * 0.068)

    return img.convert("RGB")


# ── Generate one image ────────────────────────────────────────────────────────
def generate_scene(scene_num: int, speaker: str, dialogue: str, emotion: str,
                   retries: int = 3) -> bool:
    outpath = os.path.join(OUTPUT_DIR, f"scene_{scene_num:02d}.png")
    if os.path.exists(outpath):
        print(f"  ✓ scene_{scene_num:02d} already exists – skipping")
        return True

    prompt = build_prompt(speaker, emotion)
    for attempt in range(1, retries + 1):
        try:
            print(f"  Generating scene {scene_num:02d} ({speaker}) – attempt {attempt}...")
            resp = client.images.generate(
                model=IMAGE_MODEL,
                prompt=prompt,
                size=IMAGE_SIZE,
                n=1,
            )
            item = resp.data[0]
            if item.b64_json:
                import base64
                img = Image.open(io.BytesIO(base64.b64decode(item.b64_json)))
            else:
                raw = requests.get(item.url, timeout=60).content
                img = Image.open(io.BytesIO(raw))
            img = add_text_overlay(img, scene_num, speaker, dialogue)
            img.save(outpath, "PNG")
            print(f"  ✓ Saved {outpath}")
            return True
        except Exception as e:
            print(f"  ✗ Error: {e}")
            if attempt < retries:
                wait = 2 ** attempt
                print(f"    Retrying in {wait}s...")
                time.sleep(wait)
    return False


# ── Main ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print(f"Starting generation of {len(SCENES) + 1} portrait frames...\n")
    failed = []

    for scene_num, speaker, dialogue, emotion in SCENES:
        ok = generate_scene(scene_num, speaker, dialogue, emotion)
        if not ok:
            failed.append(scene_num)
        # DALL-E 3: ~5 img/min rate limit → wait 13s between calls
        time.sleep(13)

    # Closing shot
    closing_path = os.path.join(OUTPUT_DIR, CLOSING["filename"])
    if not os.path.exists(closing_path):
        print(f"\nGenerating closing shot...")
        try:
            resp = client.images.generate(
                model=IMAGE_MODEL,
                prompt=CLOSING["prompt"],
                size=IMAGE_SIZE,
                n=1,
            )
            item = resp.data[0]
            if item.b64_json:
                import base64
                img = Image.open(io.BytesIO(base64.b64decode(item.b64_json)))
            else:
                raw = requests.get(item.url, timeout=60).content
                img = Image.open(io.BytesIO(raw))
            img.save(closing_path, "PNG")
            print(f"  ✓ Saved {closing_path}")
        except Exception as e:
            print(f"  ✗ Closing shot failed: {e}")
            failed.append(35)
        time.sleep(13)

    print(f"\n{'='*50}")
    if failed:
        print(f"Failed scenes: {failed}")
    else:
        print("All scenes generated successfully!")
    print(f"Output directory: {OUTPUT_DIR}/")
    print(f"Total files: {len(os.listdir(OUTPUT_DIR))}")
