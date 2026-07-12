import os
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import requests
from collections import defaultdict

TELEGRAM_TOKEN = "8845977529:AAExVeRs-DEwU3NOXZvrZ6rlkhtxkU9s45Q"
GROK_API_KEY = os.getenv("GROK_API_KEY")
ADMIN_ID = 1306575770  # 你的 ID

user_data = defaultdict(dict)
premium_users = set()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        ["🌸 新故事", "📜 我的故事"],
        ["📊 數值", "🖼️ 生成圖片", "💰 解鎖付費"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text("🌸 極樂後宮 AI Bot 已上線！\n付費可無限暢玩～", reply_markup=reply_markup)

async def generate_image(prompt):
    if not GROK_API_KEY:
        return None
    try:
        headers = {"Authorization": f"Bearer {GROK_API_KEY}", "Content-Type": "application/json"}
        data = {
            "model": "grok-2-image",
            "prompt": prompt + ", highly detailed, beautiful, cinematic lighting",
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

    if text == "💰 解鎖付費":
        await update.message.reply_text("付費 NT$300/月 = 無限對話 + 高品質圖片\n轉帳後告訴我，我會手動解鎖。")
        return

    if text == "🌸 新故事":
        user_data[user_id] = {"loyalty": 50, "corruption": 10, "money": 1000, "charm": 30}
        premium_users.add(user_id)  # 測試用，先給你解鎖
        await update.message.reply_text("新故事建立！請描述你的開頭設定...")
        return

    if text == "🖼️ 生成圖片":
        await update.message.reply_text("請描述想生成的畫面...")
        context.user_data["waiting_for_image"] = True
        return

    if context.user_data.get("waiting_for_image"):
        context.user_data["waiting_for_image"] = False
        await update.message.reply_text("生成中...")
        url = await generate_image(text)
        if url:
            await update.message.reply_photo(url, caption="Grok 生成")
        else:
            await update.message.reply_text("生成失敗")
        return

    if text == "📊 數值":
        data = user_data.get(user_id, {"loyalty":50,"corruption":10,"money":1000,"charm":30})
        await update.message.reply_text(f"忠誠: {data['loyalty']} | 腐化: {data['corruption']}\n金錢: {data['money']} | 魅力: {data['charm']}")
        return

    # 正常 Grok 故事生成
    await update.message.reply_text("思考中...")
    try:
        headers = {"Authorization": f"Bearer {GROK_API_KEY}", "Content-Type": "application/json"}
        data = {
            "model": "grok-4",
            "messages": [{"role": "user", "content": f"你是極樂後宮故事 AI，用非常生動、詳細、色情的方式繼續這個故事：{text}"}]
        }
        response = requests.post("https://api.x.ai/v1/chat/completions", headers=headers, json=data)
        reply = response.json()["choices"][0]["message"]["content"]
        await update.message.reply_text(reply)
    except Exception as e:
        await update.message.reply_text("AI 忙碌中... 請再試一次！")

def main():
    app = Application.builder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("addpremium", lambda u, c: premium_users.add(int(c.args[0])) if u.message.from_user.id == ADMIN_ID else None))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()

if __name__ == "__main__":
    main()
