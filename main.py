import os
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import requests
from collections import defaultdict

TELEGRAM_TOKEN = "8845977529:AAExVeRs-DEwU3NOXZvrZ6rlkhtxkU9s45Q"
GROK_API_KEY = os.getenv("GROK_API_KEY")  # 從 Railway Variables 讀取

user_data = defaultdict(dict)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        ["🌸 新故事", "📜 我的故事"],
        ["📊 數值", "🖼️ 生成圖片", "❓ 幫助"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text("🌸 極樂後宮 AI Bot 已上線！\n點選單或直接聊天～", reply_markup=reply_markup)

async def generate_image(prompt):
    if not GROK_API_KEY:
        return None
    try:
        headers = {
            "Authorization": f"Bearer {GROK_API_KEY}",
            "Content-Type": "application/json"
        }
        data = {
            "model": "grok-2-image",
            "prompt": prompt + ", beautiful detailed anime style or realistic, high quality",
            "n": 1
        }
        response = requests.post("https://api.x.ai/v1/images/generations", headers=headers, json=data, timeout=30)
        if response.status_code == 200:
            return response.json()["data"][0]["url"]
    except:
        return None
    return None

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    text = update.message.text.strip()

    if text == "🌸 新故事":
        user_data[user_id] = {"loyalty": 50, "corruption": 10, "money": 1000, "charm": 30}
        await update.message.reply_text("新故事建立！請描述你的開頭設定...")
    
    elif text == "🖼️ 生成圖片":
        await update.message.reply_text("請描述想生成的圖片場景～")
        context.user_data["waiting_for_image"] = True
    
    elif context.user_data.get("waiting_for_image"):
        context.user_data["waiting_for_image"] = False
        await update.message.reply_text("🖼️ 生成中...")
        url = await generate_image(text)
        if url:
            await update.message.reply_photo(url, caption="Grok 生成的圖片")
        else:
            await update.message.reply_text("圖片生成失敗（可能是 API Key 未設定或額度問題）")
    
    elif text == "📊 數值":
        data = user_data.get(user_id, {"loyalty":50,"corruption":10,"money":1000,"charm":30})
        await update.message.reply_text(f"忠誠: {data['loyalty']} | 腐化: {data['corruption']}\n金錢: {data['money']} | 魅力: {data['charm']}")
    
    else:
        await update.message.reply_text(f"收到：{text}\n故事繼續發展中... 你可以點「🖼️ 生成圖片」產生對應畫面喔～")

def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

if __name__ == "__main__":
    main()
