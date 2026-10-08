import os
import yt_dlp
from pyrogram import Client, filters

API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

if not API_ID or not API_HASH or not BOT_TOKEN:
    raise ValueError("Fadlan geli Environment Variables-ka saxda ah!")

DOWNLOAD_DIR = "/tmp/downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

app = Client("my_music_bot", api_id=int(API_ID), api_hash=API_HASH, bot_token=BOT_TOKEN)

@app.on_message(filters.command("start"))
def start_command(client, message):
    message.reply_text(
        "👋 Soo dhawoow! Bot-ka Music-ga ee Cloud-ka (Cookies Enabled).\n"
        "Qor magaca heesta ama link-ga si aan kuugu soo raadiyo:\n"
        "`/play [Magaca Heesta]`"
    )

@app.on_message(filters.command("play"))
async def play_audio(client, message):
    if len(message.command) < 2:
        await message.reply_text("Fadlan soo qor magaca heesta! Tusaale: `/play Somali music`")
        return

    query = message.text.split(None, 1)[1]
    status_msg = await message.reply_text(f"⏳ Waxaa la raadinayaa: *{query}*...")

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
                    'player_client': ['android', 'web'],
                }
            },
            'noplaylist': True,
            'geo_bypass': True,
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([search_query])

        if os.path.exists(output_file):
            await status_msg.edit_text("📤 Heestii waa tan, waxaa loo soo dirayaa chat-ka...")
            await message.reply_audio(audio=output_file, caption=f"🎵 {query}")
            await status_msg.delete()
        else:
            await status_msg.edit_text("❌ Khalad: Faylka audio-ga lama helin.")

    except Exception as e:
        await status_msg.edit_text(f"⚠️ Cillad: {str(e)}")

if __name__ == "__main__":
    print("🤖 Bot-ka Music-ga wuu bilaabmayaa...")
    app.run()
    
