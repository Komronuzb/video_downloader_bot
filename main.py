import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
import yt_dlp
import os

# Bot token
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Logger
logging.basicConfig(level=logging.INFO)

# Start komandasi
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Salom! Menga YouTube, TikTok, Instagram yoki Pinterest videoning havolasini yuboring.")

# Video yuklash funksiyasi
async def download_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    await update.message.reply_text("Video yuklanmoqda, biroz kuting...")

    ydl_opts = {
        'outtmpl': '%(title)s.%(ext)s',
        'format': 'bestvideo+bestaudio/best',
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            file_name = ydl.prepare_filename(info)

        await update.message.reply_video(video=open(file_name, 'rb'))
        os.remove(file_name)

    except Exception as e:
        await update.message.reply_text(f"Xatolik yuz berdi: {e}")

# Botni ishga tushirish
def main():
    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_video))

    application.run_polling()

if __name__ == "__main__":
    main()
