from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TELEGRAM_TOKEN = "8845977529:AAExVeRs-DEwU3NOXZvrZ6rlkhtxkU9s45Q"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🌸 AI 極樂後宮故事 Bot 已上線！\n\n直接聊天或輸入 /start 開始故事～")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    await update.message.reply_text(f"收到你的訊息：{text}\n\n繼續說你的故事設定，我會陪你發展極樂後宮劇情～ 🔥")

def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

if __name__ == '__main__':
    main()
