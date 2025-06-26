import os
import logging
import requests
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
)

# === CONFIG ===
BOT_TOKEN = os.getenv("BOT_TOKEN")
TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")
MODEL = "meta-llama/Llama-3.3-70B-Instruct-Turbo"

# === LOGGER ===
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

# === AI REPLY FUNCTION ===
def get_ai_reply(prompt: str) -> str:
    url = "https://api.together.xyz/inference"
    headers = {
        "Authorization": f"Bearer {TOGETHER_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "model": MODEL,
        "prompt": f"You are a helpful AI assistant. Answer clearly.\nUser: {prompt}\nAI:",
        "max_tokens": 200,
        "temperature": 0.7,
        "top_k": 50,
        "top_p": 0.9,
        "repetition_penalty": 1.1,
        "stop": ["User:", "AI:"],
    }
    try:
        res = requests.post(url, headers=headers, json=payload)
        if res.status_code == 200:
            return res.json().get("output", "🤖 I didn't catch that.")
        else:
            return f"⚠️ API Error: {res.status_code}"
    except Exception as e:
        return f"❌ Error: {e}"

# === COMMAND HANDLERS ===
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Welcome! Ask me anything with /ask command.")

async def ask(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❓ Usage: /ask What is Bitcoin?")
        return
    user_input = " ".join(context.args)
    await update.message.chat.send_action(action="typing")
    reply = get_ai_reply(user_input)
    await update.message.reply_text(reply)

# === MAIN FUNCTION ===
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("ask", ask))
    print("🤖 Simple AI Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
