
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


#TEXT WRAP FUNCTION (IMPORTANT)
def fit_text(draw, text, font, max_width):
    words = text.split()
    line = ""
    result = ""
    for w in words:
        test = line + w + " "
        if draw.textlength(test, font=font) <= max_width:
            line = test
        else:
            result += line.strip() + "\n"
            line = w + " "
    result += line.strip()
    return result


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
        title_font = ImageFont.truetype("Ayush/assets/font.ttf", 42)
        artist_font = ImageFont.truetype("Ayush/assets/font2.ttf", 28)
        bot_font = ImageFont.truetype("Ayush/assets/font2.ttf", 26)
        time_font = ImageFont.truetype("Ayush/assets/font2.ttf", 24)

        # ---------- BIGGER PLAYER CARD ----------
        card_width = 1080
        card_height = 380

        card = Image.new("RGBA", (card_width, card_height), (35, 35, 35, 200))
        mask = Image.new("L", card.size, 0)
        ImageDraw.Draw(mask).rounded_rectangle(
            (0, 0, card_width, card_height),
            radius=55,
            fill=255
        )
        bg.paste(card, (100, 190), mask)

        # ---------- ALBUM IMAGE ----------
        album = yt.resize((245, 245))
        amask = Image.new("L", album.size, 0)
        ImageDraw.Draw(amask).rounded_rectangle(
            (0, 0, 240, 240),
            radius=30,
            fill=255
        )
        bg.paste(album, (140, 250), amask)

        # ---------- TEXT AREA ----------
        x = 420
        max_text_width = 620

        title_text = fit_text(
            draw,
            clean_title(title),
            title_font,
            max_text_width
        )

        draw.multiline_text(
            (x, 250),
            title_text,
            font=title_font,
            fill="white",
            spacing=6
        )

        draw.text(
            (x, 320),
            channel,
            font=artist_font,
            fill=(200, 200, 200)
        )

        draw.text(
            (x, 355),
            "AYUSH MUSIC • PLAYING",
            font=bot_font,
            fill=(150, 150, 150)
        )

        # ---------- PROGRESS BAR ----------
        bar_y = 430
        bar_x1 = x
        bar_x2 = x + max_text_width

        draw.line(
            (bar_x1, bar_y, bar_x2, bar_y),
            fill=(100, 100, 100),
            width=4
        )

        progress_x = bar_x1 + 220
        draw.line(
            (bar_x1, bar_y, progress_x, bar_y),
            fill=(90, 170, 255),
            width=4
        )

        draw.ellipse(
            (progress_x - 5, bar_y - 5, progress_x + 5, bar_y + 5),
            fill="white"
        )

        draw.text(
            (bar_x1 - 45, bar_y + 10),
            "00:00",
            font=time_font,
            fill="white"
        )

        draw.text(
            (bar_x2 + 10, bar_y + 10),
            duration,
            font=time_font,
            fill="white"
        )

        # ---------- SAVE ----------
        bg.save(f"cache/{videoid}.png")
        os.remove(f"cache/temp_{videoid}.png")
        return f"cache/{videoid}.png"

    except Exception as e:
        print("Thumbnail error:", e)
        return YOUTUBE_IMG_URL
