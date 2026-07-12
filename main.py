import os
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import requests
from collections import defaultdict

TELEGRAM_TOKEN = "8845977529:AAExVeRs-DEwU3NOXZvrZ6rlkhtxkU9s45Q"
GROK_API_KEY = os.getenv("GROK_API_KEY")
ADMIN_ID = @willchicken

user_data = defaultdict(dict)
premium_users = set()  # 付費用戶

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        ["🌸 新故事", "📜 我的故事"],
        ["📊 數值", "🖼️ 生成圖片", "💰 解鎖付費"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text("🌸 極樂後宮 AI Bot\n付費可無限使用 + 更高品質", reply_markup=reply_markup)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    text = update.message.text.strip()

    if text == "💰 解鎖付費":
        await update.message.reply_text("付費方案：\nNT$300 / 月 = 無限對話 + 優先圖片\n\n轉帳後告知我你的用戶名，我會手動解鎖。")
    
    elif text == "🌸 新故事" or text == "📜 我的故事" or text == "📊 數值" or text == "🖼️ 生成圖片":
        if user_id not in premium_users and len(user_data.get(user_id, {})) > 0:
            await update.message.reply_text("免費用戶每日限額已達！\n點「💰 解鎖付費」成為 VIP 吧～")
            return
        # 正常流程...
        # (把之前的 handle_message 內容貼這裡)
    
    else:
        await update.message.reply_text("收到！繼續你的故事～")

# 管理員指令
async def add_premium(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.from_user.id == ADMIN_ID:
        try:
            user_to_add = int(context.args[0])
            premium_users.add(user_to_add)
            await update.message.reply_text(f"已為 {user_to_add} 開通付費！")
        except:
            await update.message.reply_text("用法：/addpremium 用戶ID")

def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("addpremium", add_premium))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

if __name__ == "__main__":
    main()
