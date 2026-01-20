import os
import re
import random
import aiofiles
import aiohttp

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont
from py_yt import VideosSearch
from config import YOUTUBE_IMG_URL

from Ayush import app

# ================= UTILS =================
def changeImageSize(maxWidth, maxHeight, image):
    ratio = max(maxWidth / image.size[0], maxHeight / image.size[1])
    return image.resize(
        (int(image.size[0] * ratio), int(image.size[1] * ratio)),
        Image.LANCZOS
    )


def clean_title(text):
    text = re.sub(r"\W+", " ", text)
    return text.strip()[:50]


# ================= NEON COLORS =================
NEON_COLORS = [
    ("#ff004f", "#ff2f7d"),  # red
    ("#ff00c8", "#ff4ddb"),  # pink
    ("#00ff99", "#4dffc3"),  # green
    ("#00aaff", "#4dc3ff"),  # blue
    ("#ffd000", "#ffe066"),  # yellow
]


# ================= MAIN =================
async def get_thumb(videoid):
    if os.path.isfile(f"cache/{videoid}.png"):
        return f"cache/{videoid}.png"

    try:
        url = f"https://www.youtube.com/watch?v={videoid}"
        results = VideosSearch(url, limit=1)
        data = (await results.next())["result"][0]

        title = clean_title(data["title"])
        duration = data.get("duration", "0:00")
        views = data.get("viewCount", {}).get("short", "Unknown")
        thumb_url = data["thumbnails"][0]["url"].split("?")[0]

        # ---------- DOWNLOAD THUMB ----------
        async with aiohttp.ClientSession() as s:
            async with s.get(thumb_url) as r:
                async with aiofiles.open("temp.png", "wb") as f:
                    await f.write(await r.read())

        yt = Image.open("temp.png").convert("RGBA")

        # ---------- BACKGROUND ----------
        bg = changeImageSize(1280, 720, yt)
        bg = bg.filter(ImageFilter.GaussianBlur(22))
        bg = ImageEnhance.Brightness(bg).enhance(0.40)

        draw = ImageDraw.Draw(bg)

        # ---------- RANDOM NEON ----------
        glow_color, border_color = random.choice(NEON_COLORS)

        # ---------- CENTER THUMB ----------
        thumb_w, thumb_h = 840, 460
        yt_thumb = yt.resize((thumb_w, thumb_h))

        mask = Image.new("L", (thumb_w, thumb_h), 0)
        ImageDraw.Draw(mask).rounded_rectangle(
            (0, 0, thumb_w, thumb_h), radius=25, fill=255
        )
        yt_thumb.putalpha(mask)

        x = (1280 - thumb_w) // 2
        y = 160

        # ---------- GLOW ----------
        glow = Image.new("RGBA", bg.size, (0, 0, 0, 0))
        gdraw = ImageDraw.Draw(glow)

        gdraw.rounded_rectangle(
            (x - 25, y - 25, x + thumb_w + 25, y + thumb_h + 25),
            radius=35,
            fill=glow_color,
        )
        glow = glow.filter(ImageFilter.GaussianBlur(35))
        bg.alpha_composite(glow)

        # ---------- BORDER ----------
        border = Image.new("RGBA", bg.size, (0, 0, 0, 0))
        bdraw = ImageDraw.Draw(border)
        bdraw.rounded_rectangle(
            (x - 6, y - 6, x + thumb_w + 6, y + thumb_h + 6),
            radius=30,
            outline=border_color,
            width=6,
        )
        bg.alpha_composite(border)

        bg.paste(yt_thumb, (x, y), yt_thumb)

        # ---------- FONTS ----------
        title_font = ImageFont.truetype("Ayush/assets/font.ttf", 46)
        info_font = ImageFont.truetype("Ayush/assets/font2.ttf", 30)
        watermark_font = ImageFont.truetype("Ayush/assets/font2.ttf", 24)

        # ---------- TITLE (TOP RIGHT) ----------
        title_w = draw.textlength(title, font=title_font)
        draw.text(
            (1280 - title_w - 40, 40),
            title,
            font=title_font,
            fill="white",
            stroke_width=2,
            stroke_fill=border_color,
        )

        # ---------- BOTTOM INFO ----------
        info_text = f"YouTube : {views} | Time : {duration} | Player : @Spotify_x_music_bot"
        info_w = draw.textlength(info_text, font=info_font)

        draw.text(
            ((1280 - info_w) // 2, y + thumb_h + 40),
            info_text,
            font=info_font,
            fill=border_color,
        )

        # ---------- WATERMARK ----------
        draw.text(
            (30, 30),
            "AYUSH MUSIC",
            font=watermark_font,
            fill=border_color,
        )

        # ---------- SAVE ----------
        bg.save(f"cache/{videoid}.png")
        os.remove("temp.png")
        return f"cache/{videoid}.png"

    except Exception as e:
        print("Thumbnail error:", e)
        return YOUTUBE_IMG_URL
