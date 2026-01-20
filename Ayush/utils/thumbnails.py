import os, re, random, aiofiles, aiohttp
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
    out = ""
    for w in text.split():
        if len(out) + len(w) < 45:
            out += " " + w
    return out.strip()


def title_font_auto(title):
    size = 46
    if len(title) > 28:
        size = 40
    if len(title) > 40:
        size = 34
    return ImageFont.truetype("Ayush/assets/font.ttf", size)


# ================= NEON COLORS =================
NEON_COLORS = [
    (255, 70, 70),     # red
    (255, 70, 200),    # pink
    (70, 255, 170),    # green
    (70, 170, 255),    # blue
    (255, 220, 70),    # yellow
]


# ================= NEON DESIGN =================
def neon_design(bg, yt, draw, title, artist, duration, fonts):
    title_font, artist_font, bot_font, time_font = fonts
    neon = random.choice(NEON_COLORS)

    # ---- CENTER IMAGE ----
    center = yt.resize((1000, 520))
    bg.paste(center, (140, 80))

    # ---- NEON BORDER ----
    overlay = Image.new("RGBA", bg.size, (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)

    for i in range(10):
        od.rounded_rectangle(
            (120-i, 60-i, 1160+i, 620+i),
            radius=45,
            outline=(*neon, 90 - i*8),
            width=3
        )

    bg.alpha_composite(overlay)

    # ---- GLOW TEXT FUNCTION ----
    def glow_text(x, y, text, font, color):
        for i in range(1, 6):
            draw.text((x+i, y), text, font=font, fill=(*color, 40))
            draw.text((x-i, y), text, font=font, fill=(*color, 40))
            draw.text((x, y+i), text, font=font, fill=(*color, 40))
            draw.text((x, y-i), text, font=font, fill=(*color, 40))
        draw.text((x, y), text, font=font, fill=color)

    # ---- TITLE ----
    glow_text(260, 340, title, title_font, neon)

    # ---- ARTIST ----
    draw.text(
        (260, 400),
        artist,
        font=artist_font,
        fill=(230, 230, 230)
    )

    # ---- BRANDING ----
    draw.text(
        (980, 90),
        "AYUSH MUSIC",
        font=bot_font,
        fill=neon
    )

    # ---- PLAYER INFO ----
    draw.text(
        (260, 610),
        f"00:00  ●━━━━━━━━━━━  {duration}",
        font=time_font,
        fill=(220, 220, 220)
    )


# ================= MAIN =================
async def get_thumb(videoid):
    try:
        res = VideosSearch(f"https://www.youtube.com/watch?v={videoid}", limit=1)
        data = (await res.next())["result"][0]

        title = clean_title(data["title"])
        artist = data["channel"]["name"]
        duration = data.get("duration", "0:00")
        thumb = data["thumbnails"][0]["url"].split("?")[0]

        async with aiohttp.ClientSession() as s:
            async with s.get(thumb) as r:
                async with aiofiles.open("temp.png", "wb") as f:
                    await f.write(await r.read())

        yt = Image.open("temp.png").convert("RGBA")

        bg = changeImageSize(1280, 720, yt)
        bg = bg.filter(ImageFilter.GaussianBlur(25))
        bg = ImageEnhance.Brightness(bg).enhance(0.45)

        draw = ImageDraw.Draw(bg)

        fonts = (
            title_font_auto(title),
            ImageFont.truetype("Ayush/assets/font2.ttf", 32),
            ImageFont.truetype("Ayush/assets/font2.ttf", 26),
            ImageFont.truetype("Ayush/assets/font2.ttf", 24),
        )

        neon_design(bg, yt, draw, title, artist, duration, fonts)

        bg.save(f"cache/{videoid}.png")
        os.remove("temp.png")
        return f"cache/{videoid}.png"

    except Exception as e:
        print("Thumbnail error:", e)
        return YOUTUBE_IMG_URL
