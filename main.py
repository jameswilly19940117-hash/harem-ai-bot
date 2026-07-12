from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from collections import defaultdict

TELEGRAM_TOKEN = "8845977529:AAExVeRs-DEwU3NOXZvrZ6rlkhtxkU9s45Q"

# 儲存用戶數據 (故事 + 數值)
user_data = defaultdict(dict)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [KeyboardButton("🌸 新故事"), KeyboardButton("📜 我的故事")],
        [KeyboardButton("📊 數值狀態"), KeyboardButton("❓ 幫助")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=False)
    
    await update.message.reply_text(
        "🌸 歡迎來到《AI 極樂後宮故事》\n\n"
        "點選選單或直接聊天開始你的專屬故事～", 
        reply_markup=reply_markup
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    text = update.message.text.strip()

    if text == "🌸 新故事":
        user_data[user_id] = {"story": "new", "loyalty": 50, "corruption": 10, "money": 1000, "charm": 30}
        await update.message.reply_text("新故事已建立！請描述你的開頭設定（例如：我是落魄貴族，想建立後宮...）")
    
    elif text == "📜 我的故事":
        data = user_data.get(user_id, {})
        if data:
            await update.message.reply_text(f"當前故事進度：\n{text[:100]}...\n\n繼續說下一步吧！")
        else:
            await update.message.reply_text("還沒有故事！點「🌸 新故事」開始～")
    
    elif text == "📊 數值狀態":
        data = user_data.get(user_id, {"loyalty": 50, "corruption": 10, "money": 1000, "charm": 30})
        await update.message.reply_text(
            f"📊 你的數值：\n"
            f"忠誠值：{data.get('loyalty', 50)}\n"
            f"腐化值：{data.get('corruption', 10)}\n"
            f"金錢：{data.get('money', 1000)}\n"
            f"魅力：{data.get('charm', 30)}"
        )
    
    elif text == "❓ 幫助":
        await update.message.reply_text("直接聊天我會根據你的描述發展故事！\n數值會隨劇情變化～")
    
    else:
        # 一般對話
        data = user_data.get(user_id, {})
        if data:
            # 簡單數值變化示範
            if "後宮" in text or "女" in text:
                data["corruption"] = min(100, data.get("corruption", 10) + 5)
            await update.message.reply_text(f"收到你的描述：{text}\n\n故事繼續發展中...（腐化值上升）")
        else:
            await update.message.reply_text("先點「🌸 新故事」開始吧！")

def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

if __name__ == "__main__":
    main()
