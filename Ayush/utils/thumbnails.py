import os
import re
import aiofiles
import aiohttp

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont
from py_yt import VideosSearch
from unidecode import unidecode

from Ayush import app
from config import YOUTUBE_IMG_URL


def changeImageSize(maxWidth, maxHeight, image):
    widthRatio = maxWidth / image.size[0]
    heightRatio = maxHeight / image.size[1]
    newWidth = int(widthRatio * image.size[0])
    newHeight = int(heightRatio * image.size[1])
    return image.resize((newWidth, newHeight), Image.LANCZOS)


def clean_title(text):
    text = re.sub(r"\W+", " ", text)
    title = ""
    for i in text.split():
        if len(title) + len(i) < 45:
            title += " " + i
    return title.strip()


async def get_thumb(videoid):
    if os.path.isfile(f"cache/{videoid}.png"):
        return f"cache/{videoid}.png"

    try:
        results = VideosSearch(
            f"https://www.youtube.com/watch?v={videoid}",
            limit=1
        )
        data = (await results.next())["result"][0]

        title = data.get("title", "Unknown Song")
        duration = data.get("duration", "0:00")
        channel = data.get("channel", {}).get("name", "Unknown Artist")
        thumb_url = data["thumbnails"][0]["url"].split("?")[0]

        # ---------- DOWNLOAD THUMB ----------
        async with aiohttp.ClientSession() as session:
            async with session.get(thumb_url) as resp:
                f = await aiofiles.open(f"cache/temp_{videoid}.png", "wb")
                await f.write(await resp.read())
                await f.close()

        # ---------- BASE IMAGE ----------
        yt = Image.open(f"cache/temp_{videoid}.png").convert("RGBA")
        bg = changeImageSize(1280, 720, yt)
        bg = bg.filter(ImageFilter.GaussianBlur(22))
        bg = ImageEnhance.Brightness(bg).enhance(0.45)

        draw = ImageDraw.Draw(bg)

        # ---------- FONTS ----------
        title_font = ImageFont.truetype("Ayush/assets/font.ttf", 44)
        artist_font = ImageFont.truetype("Ayush/assets/font2.ttf", 28)
        bot_font = ImageFont.truetype("Ayush/assets/font2.ttf", 26)
        time_font = ImageFont.truetype("Ayush/assets/font2.ttf", 24)

        # ---------- PLAYER CARD ----------
        card = Image.new("RGBA", (1040, 360), (15, 15, 15, 215))
        mask = Image.new("L", card.size, 0)
        ImageDraw.Draw(mask).rounded_rectangle(
            (0, 0, 1040, 360),
            radius=45,
            fill=255
        )
        bg.paste(card, (120, 200), mask)

        # ---------- ALBUM IMAGE ----------
        album = yt.resize((240, 240))
        amask = Image.new("L", album.size, 0)
        ImageDraw.Draw(amask).rounded_rectangle(
            (0, 0, 240, 240),
            radius=30,
            fill=255
        )
        bg.paste(album, (160, 260), amask)

        # ---------- TEXT FORMAT ----------
        x = 440

        # UNHOLY
        draw.text(
            (x, 260),
            clean_title(title),
            font=title_font,
            fill="white"
        )

        # Sam Smith & Kim Petras
        draw.text(
            (x, 315),
            channel,
            font=artist_font,
            fill=(200, 200, 200)
        )

        # AYUSH MUSIC • PLAYING
        draw.text(
            (x, 355),
            f"{unidecode(app.name)} • PLAYING",
            font=bot_font,
            fill=(170, 170, 170)
        )

        # ---------- PROGRESS BAR ----------
        bar_y = 420
        bar_x1 = x
        bar_x2 = 1040

        draw.line(
            (bar_x1, bar_y, bar_x2, bar_y),
            fill=(120, 120, 120),
            width=6
        )

        progress_x = bar_x1 + 200
        draw.line(
            (bar_x1, bar_y, progress_x, bar_y),
            fill=(90, 180, 255),
            width=6
        )

        draw.ellipse(
            (progress_x - 6, bar_y - 6, progress_x + 6, bar_y + 6),
            fill="white"
        )

        # ---------- TIME ----------
        draw.text(
            (bar_x1 - 45, bar_y + 12),
            "00:00",
            font=time_font,
            fill="white"
        )

        draw.text(
            (bar_x2 + 10, bar_y + 12),
            duration,
            font=time_font,
            fill="white"
        )

        # ---------- SAVE ----------
        bg.save(f"cache/{videoid}.png")
        os.remove(f"cache/temp_{videoid}.png")
        return f"cache/{videoid}.png"

    except Exception as e:
        print(e)
        return YOUTUBE_IMG_URL
