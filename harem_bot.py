from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import os

TELEGRAM_TOKEN = "8845977529:AAExVeRs-DEwU3NOXZvrZ6rlkhtxkU9s45Q"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🌸 雲端極樂後宮 Bot 已上線！\n直接聊天開始你的故事吧～")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    await update.message.reply_text(f"收到：{text}\n\n繼續告訴我你的後宮故事設定，我會盡力陪你發展～ 🔥")

def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("Bot started with polling")
    app.run_polling()

if __name__ == "__main__":
    main()
