async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    text = update.message.text.strip()

    if text in ["🌸 新故事", "新故事"]:
        user_data[user_id] = {"loyalty": 50, "corruption": 10, "money": 1000, "charm": 30, "history": []}
        await update.message.reply_text("新故事建立！請描述你的開頭或角色設定～")
        return

    if text in ["🖼️ 生成圖片", "生成圖片"]:
        await update.message.reply_text("請描述想生成的畫面...")
        context.user_data["waiting_for_image"] = True
        return

    if context.user_data.get("waiting_for_image"):
        context.user_data["waiting_for_image"] = False
        await update.message.reply_text("生成圖片中...")
        url = await generate_image(text)
        if url:
            await update.message.reply_photo(url)
        else:
            await update.message.reply_text("生成失敗，請稍後再試。")
        return

    # 正常故事對話 - 呼叫 Grok
    await update.message.reply_text("思考中...")
    try:
        headers = {"Authorization": f"Bearer {GROK_API_KEY}", "Content-Type": "application/json"}
        data = {
            "model": "grok-4",
            "messages": [{"role": "user", "content": f"你是極樂後宮故事 AI，用生動色情詳細方式繼續這個故事：{text}"}]
        }
        response = requests.post("https://api.x.ai/v1/chat/completions", headers=headers, json=data)
        reply = response.json()["choices"][0]["message"]["content"]
        await update.message.reply_text(reply)
    except:
        await update.message.reply_text("AI 忙碌中... 請再試一次！")
