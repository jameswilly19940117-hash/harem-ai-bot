from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TELEGRAM_TOKEN = "8845977529:AAExVeRs-DEwU3NOXZvrZ6rlkhtxkU9s45Q"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        ["🌸 開始新故事", "📊 查看狀態"],
        ["👤 角色設定", "❓ 幫助"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    
    await update.message.reply_text("🌸 歡迎來到 AI 極樂後宮故事！\n請選擇功能或直接聊天：", reply_markup=reply_markup)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    
    if text == "🌸 開始新故事":
        await update.message.reply_text("請描述你的故事開頭或角色（例如：我是皇帝，想建立後宮...）")
    elif text == "📊 查看狀態":
        await update.message.reply_text("目前狀態：\n忠誠值：50\n腐化值：10\n金錢：1000\n\n（數值系統開發中）")
    elif text == "👤 角色設定":
        await update.message.reply_text("請描述你要扮演的角色或想加入的女角色～")
    elif text == "❓ 幫助":
        await update.message.reply_text("直接聊天我會陪你發展故事！\n使用上方選單快速操作。")
    else:
        await update.message.reply_text(f"收到：{text}\n繼續發展你的極樂後宮故事吧～ 🔥")

def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

if __name__ == "__main__":
    main()
