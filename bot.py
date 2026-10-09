import os
import yt_dlp
from pyrogram import Client, filters
from pytgcalls import PyTgCalls
from pytgcalls.types import AudioPiped

API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

if not API_ID or not API_HASH or not BOT_TOKEN:
    raise ValueError("Fadlan geli Environment Variables-ka saxda ah!")

DOWNLOAD_DIR = "/tmp/downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

app = Client("my_music_bot", api_id=int(API_ID), api_hash=API_HASH, bot_token=BOT_TOKEN)
call_py = PyTgCalls(app)

@app.on_message(filters.command("start"))
def start_command(client, message):
    message.reply_text(
        "👋 Soo dhawoow! Bot-ka Voice Chat-ka ee Cloud-ka.\n"
        "Ku dar bot-ka kooxdaada, fur Voice Chat-ka, kadibna qor:\n"
        "`/play [Magaca Heesta ama Link-ga]`"
    )

@app.on_message(filters.command("play") & filters.group)
async def play_voice_chat(client, message):
    if len(message.command) < 2:
        await message.reply_text("Fadlan soo qor magaca heesta ama link-ga! Tusaale: `/play Somali music`")
        return

    query = message.text.split(None, 1)[1]
    status_msg = await message.reply_text(f"⏳ Waxaa la raadinayaa oo laga soo dejinayaa YouTube: *{query}*...")

    try:
        search_query = query
        if not search_query.startswith("http"):
            search_query = f"ytsearch1:{search_query}"

        output_template = os.path.join(DOWNLOAD_DIR, 'song')
        output_file = os.path.join(DOWNLOAD_DIR, 'song.mp3')

        if os.path.exists(output_file):
            os.remove(output_file)

        ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': output_template,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'cookiefile': 'cookies.txt',
            'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
            'extractor_args': {
                'youtube': {
                    'player_client': ['web'],
                }
            },
            'noplaylist': True,
            'playlist_items': '1',
            'geo_bypass': True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([search_query])

        if os.path.exists(output_file):
            await status_msg.edit_text("🎙️ Waxaa lagu biirayaa Voice Chat-ka kooxda...")
            
            await call_py.join_group_call(
                message.chat.id,
                AudioPiped(output_file)
            )
            await status_msg.edit_text(f"🎵 Hadda heestu waxay ka socotaa Voice Chat-ka: *{query}*")
        else:
            await status_msg.edit_text("❌ Khalad: Faylka audio-ga lama helin.")

    except Exception as e:
        await status_msg.edit_text(f"⚠️ Cillad: {str(e)}")

@app.on_message(filters.command("stop") & filters.group)
async def stop_voice_chat(client, message):
    try:
        await call_py.leave_group_call(message.chat.id)
        await message.reply_text("🛑 Waa la joojiyay Voice Chat-kii, bot-na wuu ka baxay.")
    except Exception as e:
        await message.reply_text(f"Khalad: {str(e)}")

if __name__ == "__main__":
    print("🤖 Bot-ka Voice Chat wuu bilaabmayaa Cloud-ka...")
    app.start()
    call_py.start()
    import pyrogram
    pyrogram.idle()
    
