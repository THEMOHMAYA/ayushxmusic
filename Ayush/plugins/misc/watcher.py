from pyrogram import filters
from pyrogram.types import Message
from Ayush import app
from Ayush.core.call import Aayu

# Assign priority for handlers
WELCOME_GROUP = 20
CLOSE_GROUP = 30

@app.on_message(filters.video_chat_started, group=WELCOME_GROUP)
@app.on_message(filters.video_chat_ended, group=CLOSE_GROUP)
async def auto_stop_stream(_, message: Message):
    """
    Automatically stop the active stream when a video chat starts or ends.
    """
    chat_id = message.chat.id
    try:
        await Aayu.stop_stream_force(chat_id)
    except Exception as e:
        print(f"[AUTO STOP] Error stopping stream in chat {chat_id}: {e}")
