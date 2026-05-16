import logging
import os
import tempfile
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import yt_dlp

BOT_TOKEN = "8967489541:AAEeiyJ1hxHCUeHU80ktv3nX4XmKuKwHZ9w"

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Salom! Instagram video havolasini yuboring!")

async def download_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()
    if "instagram.com" not in url:
        await update.message.reply_text("❌ Instagram havolasini yuboring!")
        return
    msg = await update.message.reply_text("⏳ Yuklanmoqda...")
    try:
        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = os.path.join(tmpdir, "video.mp4")
            ydl_opts = {"outtmpl": output_path, "format": "best[ext=mp4]/best", "quiet": True}
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            files = os.listdir(tmpdir)
            if files:
                output_path = os.path.join(tmpdir, files[0])
            with open(output_path, "rb") as f:
                await update.message.reply_video(video=f, caption="✅ Mana videongiz!")
            await msg.delete()
    except Exception as e:
        await msg.edit_text("❌ Video yuklab bolmadi.")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_video))
    app.run_polling()

if __name__ == "__main__":
    main()
