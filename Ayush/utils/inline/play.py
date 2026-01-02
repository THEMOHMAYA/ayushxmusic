import math
from config import SUPPORT_CHAT, OWNER_ID
from pyrogram.types import InlineKeyboardButton
from Ayush.utils.formatters import time_to_seconds


# -------------------------------- TRACK MARKUP -------------------------------- #
def track_markup(_, videoid, user_id, channel, fplay):
    buttons = [
        [
            InlineKeyboardButton(
                text=_["P_B_1"],  # Play Audio
                callback_data=f"MusicStream {videoid}|{user_id}|a|{channel}|{fplay}",
            ),
            InlineKeyboardButton(
                text=_["P_B_2"],  # Play Video
                callback_data=f"MusicStream {videoid}|{user_id}|v|{channel}|{fplay}",
            ),
        ],
        [
            InlineKeyboardButton(text="ᴏᴡɴᴇʀ", url=f"tg://openmessage?user_id={OWNER_ID}"),
            InlineKeyboardButton(text="sᴜᴩᴩᴏʀᴛ", url=SUPPORT_CHAT),
        ],
        [InlineKeyboardButton(text=_["CLOSE_BUTTON"], callback_data=f"forceclose {videoid}|{user_id}")],
    ]
    return buttons


# ----------------------------- SPOTIFY STYLE TIMER --------------------------- #
def stream_markup_timer(_, chat_id, played, dur):
    played_sec = time_to_seconds(played)
    duration_sec = time_to_seconds(dur)
    percentage = (played_sec / duration_sec) * 100
    umm = math.floor(percentage)
    if 0 < umm <= 10:
        bar = "▶—————————"
    elif 10 < umm < 20:
        bar = "—◉————————"
    elif 20 <= umm < 30:
        bar = "——◉———————"
    elif 30 <= umm < 40:
        bar = "———◉——————"
    elif 40 <= umm < 50:
        bar = "————◉—————"
    elif 50 <= umm < 60:
        bar = "—————◉————"
    elif 60 <= umm < 70:
        bar = "——————◉———"
    elif 70 <= umm < 80:
        bar = "———————◉——"
    elif 80 <= umm < 95:
        bar = "————————◉—"
    else:
        bar = "—————————▶"
    buttons = [
        # Progress bar row
        [
            InlineKeyboardButton(text=f"{played} {bar} {dur}", callback_data="GetTimer")
        ],
        # Main controls
        [
            InlineKeyboardButton(text="▷", callback_data=f"ADMIN Resume|{chat_id}"),
            InlineKeyboardButton(text="II", callback_data=f"ADMIN Pause|{chat_id}"),
            InlineKeyboardButton(text="‣‣I", callback_data=f"ADMIN Skip|{chat_id}"),
            InlineKeyboardButton(text="▢", callback_data=f"ADMIN Stop|{chat_id}"),
        ],
        # Replay, Owner, Support
        [
            InlineKeyboardButton(text="↻ Replay", callback_data=f"ADMIN Replay|{chat_id}"),
            InlineKeyboardButton(text="Owner", url=f"tg://openmessage?user_id={OWNER_ID}"),
            InlineKeyboardButton(text="Support", url=SUPPORT_CHAT),
        ],
        # Listening Now row (7th feature)
        [
            InlineKeyboardButton(text=f"{listeners} Listening Now", callback_data="listening_now")
        ] if listeners else [],
        # Close button
        [InlineKeyboardButton(text=_["CLOSE_BUTTON"], callback_data="close")],
    ]
    # Remove empty rows
    buttons = [row for row in buttons if row]
    return buttons


# ----------------------------- SIMPLE STREAM MARKUP -------------------------- #
def stream_markup(_, chat_id):
    buttons = [
        [
            InlineKeyboardButton(text="▷", callback_data=f"ADMIN Resume|{chat_id}"),
            InlineKeyboardButton(text="II", callback_data=f"ADMIN Pause|{chat_id}"),
            InlineKeyboardButton(text="↻", callback_data=f"ADMIN Replay|{chat_id}"),
            InlineKeyboardButton(text="‣‣I", callback_data=f"ADMIN Skip|{chat_id}"),
            InlineKeyboardButton(text="▢", callback_data=f"ADMIN Stop|{chat_id}"),
        ],
        [
            InlineKeyboardButton(text="ᴏᴡɴᴇʀ", url=f"tg://openmessage?user_id={OWNER_ID}"),
            InlineKeyboardButton(text="sᴜᴩᴩᴏʀᴛ", url=SUPPORT_CHAT),
        ],
        [InlineKeyboardButton(text=_["CLOSE_BUTTON"], callback_data="close")],
    ]
    return buttons


# ----------------------------- PLAYLIST MARKUP ------------------------------- #
def playlist_markup(_, videoid, user_id, ptype, channel, fplay):
    buttons = [
        [
            InlineKeyboardButton(
                text=_["P_B_1"], callback_data=f"AayuPlaylists {videoid}|{user_id}|{ptype}|a|{channel}|{fplay}"
            ),
            InlineKeyboardButton(
                text=_["P_B_2"], callback_data=f"AayuPlaylists {videoid}|{user_id}|{ptype}|v|{channel}|{fplay}"
            ),
        ],
        [InlineKeyboardButton(text=_["CLOSE_BUTTON"], callback_data=f"forceclose {videoid}|{user_id}")],
    ]
    return buttons


# ----------------------------- LIVE STREAM MARKUP ---------------------------- #
def livestream_markup(_, videoid, user_id, mode, channel, fplay):
    buttons = [
        [
            InlineKeyboardButton(
                text=_["P_B_3"], callback_data=f"LiveStream {videoid}|{user_id}|{mode}|{channel}|{fplay}"
            ),
        ],
        [InlineKeyboardButton(text=_["CLOSE_BUTTON"], callback_data=f"forceclose {videoid}|{user_id}")],
    ]
    return buttons


# ----------------------------- SLIDER MARKUP -------------------------------- #
def slider_markup(_, videoid, user_id, query, query_type, channel, fplay):
    query = query[:20]
    buttons = [
        [
            InlineKeyboardButton(
                text=_["P_B_1"], callback_data=f"MusicStream {videoid}|{user_id}|a|{channel}|{fplay}"
            ),
            InlineKeyboardButton(
                text=_["P_B_2"], callback_data=f"MusicStream {videoid}|{user_id}|v|{channel}|{fplay}"
            ),
        ],
        [
            InlineKeyboardButton(
                text="◁", callback_data=f"slider B|{query_type}|{query}|{user_id}|{channel}|{fplay}"
            ),
            InlineKeyboardButton(text=_["CLOSE_BUTTON"], callback_data=f"forceclose {query}|{user_id}"),
            InlineKeyboardButton(
                text="▷", callback_data=f"slider F|{query_type}|{query}|{user_id}|{channel}|{fplay}"
            ),
        ],
    ]
    return buttons
