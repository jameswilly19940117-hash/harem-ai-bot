from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import os

TELEGRAM_TOKEN = "8845977529:AAExVeRs-DEwU3NOXZvrZ6rlkhtxkU9s45Q"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🌸 雲端極樂後宮 Bot 已上線！")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    await update.message.reply_text(f"收到：{text}\n繼續你的後宮故事吧～")

def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Webhook mode for Render
    port = int(os.environ.get("PORT", 8443))
    app.run_webhook(listen="0.0.0.0", port=port, url_path=TELEGRAM_TOKEN)

if __name__ == "__main__":
    main()
