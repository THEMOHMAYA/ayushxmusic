
import os
import re
import aiofiles
import aiohttp

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont
from py_yt import VideosSearch
from config import YOUTUBE_IMG_URL

from Ayush import app
from config import YOUTUBE_IMG_URL


def changeImageSize(maxWidth, maxHeight, image):
    ratio = max(maxWidth / image.size[0], maxHeight / image.size[1])
    size = (int(image.size[0] * ratio), int(image.size[1] * ratio))
    return image.resize(size, Image.LANCZOS)


def clean_title(text):
    text = re.sub(r"\W+", " ", text)
    title = ""
    for i in text.split():
        if len(title) + len(i) < 50:
            title += " " + i
    return title.strip()


def fit_text(draw, text, font, max_width):
    words = text.split()
    line, result = "", ""
    for w in words:
        test = line + w + " "
        if draw.textlength(test, font=font) <= max_width:
            line = test
        else:
            result += line.strip() + "\n"
            line = w + " "
    return result + line.strip()


async def get_thumb(videoid):
    if os.path.isfile(f"cache/{videoid}.png"):
        return f"cache/{videoid}.png"

    try:
        results = VideosSearch(f"https://www.youtube.com/watch?v={videoid}", limit=1)
        data = (await results.next())["result"][0]

        title = data.get("title", "Unknown Song")
        duration = data.get("duration", "0:00")
        channel = data.get("channel", {}).get("name", "Unknown Artist")
        thumb_url = data["thumbnails"][0]["url"].split("?")[0]

        # -------- DOWNLOAD THUMB --------
        async with aiohttp.ClientSession() as session:
            async with session.get(thumb_url) as resp:
                async with aiofiles.open(f"cache/temp_{videoid}.png", "wb") as f:
                    await f.write(await resp.read())

        yt = Image.open(f"cache/temp_{videoid}.png").convert("RGBA")

        # -------- BACKGROUND --------
        bg = changeImageSize(1280, 720, yt)
        bg = bg.filter(ImageFilter.GaussianBlur(22))
        bg = ImageEnhance.Brightness(bg).enhance(0.45)

        draw = ImageDraw.Draw(bg)

        # -------- FONTS --------
        title_font = ImageFont.truetype("Ayush/assets/font.ttf", 44)
        artist_font = ImageFont.truetype("Ayush/assets/font2.ttf", 30)
        bot_font = ImageFont.truetype("Ayush/assets/font2.ttf", 26)
        time_font = ImageFont.truetype("Ayush/assets/font2.ttf", 24)

        # -------- PLAYER CARD (BIGGER) --------
        card_width, card_height = 1120, 420
        card_x, card_y = 80, 170

        card = Image.new("RGBA", (card_width, card_height), (35, 35, 35, 210))
        mask = Image.new("L", (card_width, card_height), 0)
        ImageDraw.Draw(mask).rounded_rectangle(
            (0, 0, card_width, card_height), radius=60, fill=255
        )
        bg.paste(card, (card_x, card_y), mask)

        # -------- ALBUM IMAGE (BIGGER) --------
        album_size = 270
        album = yt.resize((album_size, album_size))
        amask = Image.new("L", (album_size, album_size), 0)
        ImageDraw.Draw(amask).rounded_rectangle(
            (0, 0, album_size, album_size), radius=35, fill=255
        )
        bg.paste(album, (120, 235), amask)

        # -------- TEXT AREA --------
        x = 420
        max_text_width = 650

        draw.multiline_text(
            (x, 240),
            fit_text(draw, clean_title(title), title_font, max_text_width),
            font=title_font,
            fill="white",
            spacing=6,
        )

        draw.text(
            (x, 315),
            channel,
            font=artist_font,
            fill=(210, 210, 210),
        )

        draw.text(
            (x, 350),
            "AYUSH MUSIC • PLAYING",
            font=bot_font,
            fill=(160, 160, 160),
        )

        # -------- PROGRESS BAR --------
        bar_y = 415
        bar_start = x + 20
        bar_end = x + max_text_width - 20

        draw.line((bar_start, bar_y, bar_end, bar_y), fill=(120, 120, 120), width=4)

        progress_x = bar_start + 240
        draw.line((bar_start, bar_y, progress_x, bar_y), fill=(90, 170, 255), width=4)

        draw.ellipse(
            (progress_x - 6, bar_y - 6, progress_x + 6, bar_y + 6),
            fill="white",
        )

        # -------- TIME (SAFE POSITION) --------
        draw.text(
            (bar_start, bar_y + 12),
            "00:00",
            font=time_font,
            fill="white",
        )

        draw.text(
            (bar_end - 40, bar_y + 12),
            duration,
            font=time_font,
            fill="white",
        )

        # -------- SAVE --------
        bg.save(f"cache/{videoid}.png")
        os.remove(f"cache/temp_{videoid}.png")
        return f"cache/{videoid}.png"

    except Exception as e:
        print("Thumbnail error:", e)
        return YOUTUBE_IMG_URL
