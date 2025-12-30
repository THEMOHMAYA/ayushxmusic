import os
import re
import aiohttp
import aiofiles

from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont
from unidecode import unidecode

from config import YOUTUBE_IMG_URL

# try import (safe)
try:
    from py_yt import VideosSearch
except Exception:
    VideosSearch = None


def clean_text(text, limit=40):
    text = unidecode(text)
    words = text.split()
    out = ""
    for w in words:
        if len(out) + len(w) <= limit:
            out += " " + w
    return out.strip()


async def get_thumb(videoid, chat_id=None):
    cache_path = f"cache/{videoid}.png"
    if os.path.isfile(cache_path):
        return cache_path

    try:
        title = "unknown title"
        duration = "00:00"
        thumb_url = YOUTUBE_IMG_URL

        # fetch youtube data
        if VideosSearch:
            search = VideosSearch(
                f"https://www.youtube.com/watch?v={videoid}", limit=1
            )
            data = (await search.next())["result"][0]
            title = clean_text(
                re.sub(r"\W+", " ", data.get("title", title))
            )
            duration = data.get("duration", duration)
            thumb_url = data["thumbnails"][0]["url"].split("?")[0]

        # download thumbnail
        async with aiohttp.ClientSession() as session:
            async with session.get(thumb_url) as resp:
                if resp.status != 200:
                    return YOUTUBE_IMG_URL
                img_bytes = await resp.read()

        temp_thumb = f"cache/temp_{videoid}.jpg"
        async with aiofiles.open(temp_thumb, "wb") as f:
            await f.write(img_bytes)

        base = Image.open(temp_thumb).convert("RGB").resize((1280, 720))

        # background blur
        bg = base.filter(ImageFilter.GaussianBlur(20))
        bg = ImageEnhance.Brightness(bg).enhance(0.55)

        draw = ImageDraw.Draw(bg)

        # fonts
        title_font = ImageFont.truetype("assets/font.ttf", 40)
        small_font = ImageFont.truetype("assets/font2.ttf", 26)

        # card
        card_x1, card_y1 = 140, 220
        card_x2, card_y2 = 1140, 520

        card = Image.new(
            "RGBA",
            (card_x2 - card_x1, card_y2 - card_y1),
            (0, 0, 0, 180),
        )
        bg.paste(card, (card_x1, card_y1), card)

        # song image
        song_img = base.resize((220, 220))
        bg.paste(song_img, (card_x1 + 25, card_y1 + 30))

        text_x = card_x1 + 270

        # title
        draw.text(
            (text_x, card_y1 + 45),
            title,
            fill="white",
            font=title_font,
        )

        # artist / bot name
        draw.text(
            (text_x, card_y1 + 100),
            "ayush music",
            fill="#b3b3b3",
            font=small_font,
        )

        # playing text
        draw.text(
            (text_x, card_y1 + 135),
            "playing",
            fill="#1db954",
            font=small_font,
        )

        # vc listeners
        listeners = get_listeners(chat_id) if chat_id else 0
        draw.text(
            (text_x, card_y1 + 170),
            f"{listeners} listening now",
            fill="#b3b3b3",
            font=small_font,
        )

        # progress bar (spotify style)
        bar_y = card_y2 - 55
        draw.text(
            (card_x1 + 25, bar_y),
            "00:00",
            fill="white",
            font=small_font,
        )
        draw.text(
            (card_x2 - 70, bar_y),
            duration,
            fill="white",
            font=small_font,
        )

        draw.line(
            [(card_x1 + 90, bar_y + 15),
             (card_x2 - 110, bar_y + 15)],
            fill="#404040",
            width=4,
        )

        draw.ellipse(
            [(card_x1 + 90, bar_y + 11),
             (card_x1 + 98, bar_y + 19)],
            fill="white",
        )

        # cleanup
        try:
            os.remove(temp_thumb)
        except Exception:
            pass

        bg.save(cache_path)
        return cache_path

    except Exception as e:
        print("thumbnail error:", e)
        return YOUTUBE_IMG_URL
