import os, re, random, aiofiles, aiohttp
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont
from py_yt import VideosSearch
from config import YOUTUBE_IMG_URL

from Ayush import app


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
        if len(out) + len(w) < 50:
            out += " " + w
    return out.strip()


def fit_text(draw, text, font, max_width):
    words, line, res = text.split(), "", ""
    for w in words:
        test = line + w + " "
        if draw.textlength(test, font=font) <= max_width:
            line = test
        else:
            res += line.strip() + "\n"
            line = w + " "
    return res + line.strip()


# ================= DESIGN 1 =================
def design_one(bg, yt, draw, title, artist, duration, fonts):
    title_font, artist_font, bot_font, time_font = fonts

    card = Image.new("RGBA", (1120, 420), (35, 35, 35, 210))
    mask = Image.new("L", card.size, 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, 1120, 420), 60, fill=255)
    bg.paste(card, (80, 170), mask)

    album = yt.resize((270, 270))
    am = Image.new("L", album.size, 0)
    ImageDraw.Draw(am).rounded_rectangle((0, 0, 270, 270), 35, fill=255)
    bg.paste(album, (120, 235), am)

    x = 420
    draw.multiline_text((x, 240),
        fit_text(draw, title, title_font, 650),
        font=title_font, fill="white", spacing=6)

    draw.text((x, 335), artist, font=artist_font, fill=(210, 210, 210))
    draw.text((x, 360), "AYUSH MUSIC • PLAYING", font=bot_font, fill=(160, 160, 160))

    bar_y = 415
    draw.line((x+20, bar_y, x+630, bar_y), fill=(120,120,120), width=4)
    draw.line((x+20, bar_y, x+260, bar_y), fill=(90,170,255), width=4)

    draw.text((x+20, bar_y+12), "00:00", font=time_font, fill="white")
    draw.text((x+580, bar_y+12), duration, font=time_font, fill="white")


# ================= DESIGN 2 =================
def design_two(bg, yt, draw, title, artist, duration, fonts):
    title_font, artist_font, bot_font, time_font = fonts

    album = yt.resize((320, 320))
    bg.paste(album, (480, 150))

    draw.text((360, 500), title[:40], font=title_font, fill="white")
    draw.text((360, 545), artist, font=artist_font, fill=(200,200,200))
    draw.text((360, 575), "AYUSH MUSIC • PLAYING", font=bot_font, fill=(160,160,160))


# ================= DESIGN 3 =================
def design_three(bg, yt, draw, title, artist, duration, fonts):
    title_font, artist_font, bot_font, time_font = fonts

    card = Image.new("RGBA", (1280, 260), (0, 0, 0, 180))
    bg.paste(card, (0, 460))

    album = yt.resize((200, 200))
    bg.paste(album, (40, 490))

    draw.text((270, 500), title, font=title_font, fill="white")
    draw.text((270, 550), artist, font=artist_font, fill=(200,200,200))
    draw.text((270, 585), "AYUSH MUSIC • PLAYING", font=bot_font, fill=(150,150,150))


# ================= DESIGN 4 =================
def design_four(bg, yt, draw, title, artist, duration, fonts):
    title_font, artist_font, bot_font, time_font = fonts

    album = yt.resize((260,260))
    bg.paste(album, (900, 230))

    draw.text((120, 260), title, font=title_font, fill="white")
    draw.text((120, 320), artist, font=artist_font, fill=(200,200,200))
    draw.text((120, 350), "AYUSH MUSIC • PLAYING", font=bot_font, fill=(160,160,160))


# ================= DESIGN 5 =================
def design_five(bg, yt, draw, title, artist, duration, fonts):
    title_font, artist_font, bot_font, time_font = fonts

    draw.rectangle((200, 180, 1080, 540), fill=(30,30,30,200))
    album = yt.resize((240,240))
    bg.paste(album, (220, 230))

    draw.text((500, 260), title, font=title_font, fill="white")
    draw.text((500, 320), artist, font=artist_font, fill=(210,210,210))
    draw.text((500, 350), "AYUSH MUSIC • PLAYING", font=bot_font, fill=(150,150,150))


# ================= MAIN FUNCTION =================
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
        bg = bg.filter(ImageFilter.GaussianBlur(22))
        bg = ImageEnhance.Brightness(bg).enhance(0.45)

        draw = ImageDraw.Draw(bg)

        fonts = (
            ImageFont.truetype("Ayush/assets/font.ttf", 44),
            ImageFont.truetype("Ayush/assets/font2.ttf", 30),
            ImageFont.truetype("Ayush/assets/font2.ttf", 26),
            ImageFont.truetype("Ayush/assets/font2.ttf", 24),
        )

        random.choice([
            design_one,
            design_two,
            design_three,
            design_four,
            design_five
        ])(bg, yt, draw, title, artist, duration, fonts)

        bg.save(f"cache/{videoid}.png")
        os.remove("temp.png")
        return f"cache/{videoid}.png"

    except Exception as e:
        print(e)
        return YOUTUBE_IMG_URL
