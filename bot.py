import logging
import os
import tempfile
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import yt_dlp

BOT_TOKEN = "8967489541:AAHhPpOZm-XZRHYl2cOfRBbGeSQTVburZJQ"

logging.basicConfig(level=logging.INFO)
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
            ydl_opts = {
                "outtmpl": os.path.join(tmpdir, "%(id)s.%(ext)s"),
                "format": "best[ext=mp4]/best",
                "quiet": True
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            files = os.listdir(tmpdir)
            if not files:
                await msg.edit_text("❌ Video topilmadi.")
                return
            filepath = os.path.join(tmpdir, files[0])
            with open(filepath, "rb") as f:
                await update.message.reply_video(video=f, caption="✅ Mana videongiz!")
            await msg.delete()
    except Exception as e:
        logger.error(e)
        await msg.edit_text("❌ Video yuklab bolmadi.")

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_video))
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
