import os
import yt_dlp
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")"  

async def download_video(url: str, format_id="best") -> str:
    ydl_opts = {
        'outtmpl': 'downloads/%(title)s.%(ext)s',
        'format': format_id,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        return ydl.prepare_filename(info)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Link yuboring (YouTube, TikTok, Instagram, Pinterest)...")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    keyboard = [
        [InlineKeyboardButton("Video yuklash", callback_data=f"video|{url}"),
         InlineKeyboardButton("Audio yuklash", callback_data=f"audio|{url}")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Nimani yuklamoqchisiz?", reply_markup=reply_markup)

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    action, url = query.data.split("|")
    format_id = "bestaudio" if action == "audio" else "best"
    file_path = await download_video(url, format_id)
    await query.edit_message_text("Yuklab olindi, yuborilyapti...")
    await context.bot.send_document(chat_id=query.message.chat_id, document=open(file_path, 'rb'))
    os.remove(file_path)

if __name__ == '__main__':
    os.makedirs("downloads", exist_ok=True)
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(CallbackQueryHandler(button))
    app.run_polling()
