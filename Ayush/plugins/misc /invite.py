from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.enums import ChatMemberStatus

from Ayush import app
from config import BANNED_USERS


# ---------------- VC STARTED ----------------
@app.on_message(filters.video_chat_started & filters.group & ~BANNED_USERS, group=10)
async def vc_started(client, message: Message):
    try:
        user = message.from_user
        chat = message.chat

        text = f"""<blockquote>
<b>ᴠɪᴅᴇᴏ ᴄʜᴀᴛ sᴛᴀʀᴛᴇᴅ</b>
━━━━━━━━━━━━━━
<b>👤 sᴛᴀʀᴛᴇᴅ ʙʏ:</b> {user.mention}
<b>🆔 ᴜsᴇʀ ɪᴅ:</b> <code>{user.id}</code>
<b>👥 ɢʀᴏᴜᴘ:</b> {chat.title}
━━━━━━━━━━━━━━
<i>🎧 ᴊᴏɪɴ ᴛʜᴇ ᴠᴏɪᴄᴇ ᴄʜᴀᴛ ɴᴏᴡ!</i>
</blockquote>"""

        buttons = None
        if chat.username:
            buttons = InlineKeyboardMarkup(
                [[
                    InlineKeyboardButton(
                        "💘 ᴊᴏɪɴ ᴠᴄ 💘",
                        url=f"https://t.me/{chat.username}?videochat"
                    )
                ]]
            )

        await message.reply_text(text, reply_markup=buttons)

    except Exception as e:
        print(f"[VC START] Error: {e}")


# ---------------- VC ENDED ----------------
@app.on_message(filters.video_chat_ended & filters.group & ~BANNED_USERS, group=10)
async def vc_ended(client, message: Message):
    try:
        user = message.from_user
        chat = message.chat
        duration = message.video_chat_ended.duration

        hours = duration // 3600
        minutes = (duration % 3600) // 60
        seconds = duration % 60

        duration_str = (
            f"{hours}h {minutes}m {seconds}s"
            if hours > 0
            else f"{minutes}m {seconds}s"
            if minutes > 0
            else f"{seconds}s"
        )

        text = f"""<blockquote>
<b>ᴠɪᴅᴇᴏ ᴄʜᴀᴛ ᴇɴᴅᴇᴅ</b>
━━━━━━━━━━━━━━
<b>👤 ᴇɴᴅᴇᴅ ʙʏ:</b> {user.mention}
<b>🆔 ᴜsᴇʀ ɪᴅ:</b> <code>{user.id}</code>
<b>⏱ ᴅᴜʀᴀᴛɪᴏɴ:</b> {duration_str}
<b>👥 ɢʀᴏᴜᴘ:</b> {chat.title}
━━━━━━━━━━━━━━
</blockquote>"""

        await message.reply_text(text)

    except Exception as e:
        print(f"[VC END] Error: {e}")


# ---------------- VC INVITE (FIXED) ----------------
@app.on_message(filters.video_chat_members_invited & filters.group & ~BANNED_USERS, group=10)
async def vc_invite(client, message: Message):
    try:
        inviter = message.from_user
        chat = message.chat
        invited_users = message.video_chat_members_invited.users

        buttons = None
        if chat.username:
            buttons = InlineKeyboardMarkup(
                [[
                    InlineKeyboardButton(
                        "🎧 ᴊᴏɪɴ ᴠᴄ",
                        url=f"https://t.me/{chat.username}?voicechat"
                    )
                ]]
            )

        for invited_user in invited_users:
            text = f"""
<blockquote>
🥂 {inviter.mention} ɪɴᴠɪᴛᴇᴅ {invited_user.mention}
ᴛᴏ ᴠᴏɪᴄᴇ ᴄʜᴀᴛ
</blockquote>
"""

            await message.reply_text(
                text,
                reply_markup=buttons
            )

    except Exception as e:
        print(f"[VC INVITE] Error: {e}")
