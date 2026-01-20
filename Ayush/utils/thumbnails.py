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
    (255, 0, 180),   # pink
    (0, 255, 200),   # green
    (0, 160, 255),   # blue
    (255, 220, 70),  # yellow
    (255, 70, 70),   # red
]


# ================= NEON DESIGN =================
def neon_design(bg, yt, title, artist, duration, views):
    draw = ImageDraw.Draw(bg)
    neon = random.choice(NEON_COLORS)

    # ---- CENTER IMAGE ----
    thumb = yt.resize((980, 500))
    bg.paste(thumb, (150, 100))

    # ---- NEON BORDER ----
    overlay = Image.new("RGBA", bg.size, (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)

    for i in range(12):
        od.rounded_rectangle(
            (120 - i, 70 - i, 1160 + i, 610 + i),
            radius=40,
            outline=(*neon, 90 - i * 6),
            width=3
        )

    bg.alpha_composite(overlay)

    # ---- FONTS ----
    title_font = title_font_auto(title)
    artist_font = ImageFont.truetype("Ayush/assets/font2.ttf", 28)
    bottom_font = ImageFont.truetype("Ayush/assets/font2.ttf", 24)
    brand_font = ImageFont.truetype("Ayush/assets/font2.ttf", 26)

    # ---- TITLE (TOP RIGHT) ----
    draw.text(
        (1120, 45),
        title,
        font=title_font,
        fill=(255, 255, 255),
        anchor="ra"
    )

    # ---- ARTIST (UNDER TITLE) ----
    draw.text(
        (1120, 85),
        artist,
        font=artist_font,
        fill=(210, 210, 210),
        anchor="ra"
    )

    # ---- BRAND ----
    draw.text(
        (1120, 125),
        "AYUSH MUSIC",
        font=brand_font,
        fill=neon,
        anchor="ra"
    )

    # ---- BOTTOM INFO ----
    bottom_text = (
        f"YouTube : {views} | "
        f"Time : {duration} | "
        f"Player : @Spotify_x_music_bot"
    )

    draw.text(
        (640, 680),
        bottom_text,
        font=bottom_font,
        fill=neon,
        anchor="mm"
    )


# ================= MAIN =================
async def get_thumb(videoid):
    try:
        res = VideosSearch(f"https://www.youtube.com/watch?v={videoid}", limit=1)
        data = (await res.next())["result"][0]

        title = clean_title(data["title"])
        artist = data["channel"]["name"]
        duration = data.get("duration", "0:00")
        views = data.get("viewCount", {}).get("text", "0 views")
        thumb = data["thumbnails"][0]["url"].split("?")[0]

        async with aiohttp.ClientSession() as s:
            async with s.get(thumb) as r:
                async with aiofiles.open("temp.png", "wb") as f:
                    await f.write(await r.read())

        yt = Image.open("temp.png").convert("RGBA")

        bg = changeImageSize(1280, 720, yt)
        bg = bg.filter(ImageFilter.GaussianBlur(28))
        bg = ImageEnhance.Brightness(bg).enhance(0.45)

        neon_design(bg, yt, title, artist, duration, views)

        path = f"cache/{videoid}.png"
        bg.save(path, quality=95)
        os.remove("temp.png")
        return path

    except Exception as e:
        print("Thumbnail error:", e)
        return YOUTUBE_IMG_URL
