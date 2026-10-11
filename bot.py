import os
import yt_dlp
from pyrogram import Client, filters
from pytgcalls import PyTgCalls
from pytgcalls.types import AudioPiped

API_ID = 37183926
API_HASH = "3153aac9e009e4e2336aa2cf963382bc"
BOT_TOKEN = "8952879139:AAHW7FIoqV9uZ9FSF4WG5UKIYor_n7gyWac"

DOWNLOAD_DIR = "/tmp/downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

app = Client(
    "voice_music_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

call_py = PyTgCalls(app)

@app.on_message(filters.command("start"))
def start_command(client, message):
    message.reply_text("👋 Bot-ka Voice Chat-ka waa diyaar! Qor `/play [magaca heesta]`")

@app.on_message(filters.command("play") & filters.group)
async def play_music(client, message):
    if len(message.command) < 2:
        await message.reply_text("❌ Fadlan qor magaca heesta!")
        return

    query = message.text.split(None, 1)[1]
    status_msg = await message.reply_text(f"⏳ Waxaa la raadinayaa: *{query}*...")

    try:
        search_query = query if query.startswith("http") else f"ytsearch1:{query}"
        output_file = os.path.join(DOWNLOAD_DIR, 'song.mp3')

        if os.path.exists(output_file):
            os.remove(output_file)

        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(DOWNLOAD_DIR, 'song'),
            'postprocessors': [{'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': '192'}],
            'noplaylist': True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([search_query])

        if os.path.exists(output_file):
            await status_msg.edit_text("🎙️ Waxaa lagu biirayaa Voice Chat-ka...")
            await call_py.join_group_call(message.chat.id, AudioPiped(output_file))
            await status_msg.edit_text(f"🎵 Hadda heestu waxay ka socotaa Voice Chat-ka: *{query}*")
        else:
            await status_msg.edit_text("❌ Faylka lama helin.")
    except Exception as e:
        await status_msg.edit_text(f"⚠️ Cillad: `{str(e)}`")

@app.on_message(filters.command("stop") & filters.group)
async def stop_music(client, message):
    try:
        await call_py.leave_group_call(message.chat.id)
        await message.reply_text("🛑 Waa la joojiyay heestii.")
    except Exception as e:
        await message.reply_text(f"Khalad: {str(e)}")

if __name__ == "__main__":
    app.start()
    call_py.start()
    import pyrogram
    pyrogram.idle()
