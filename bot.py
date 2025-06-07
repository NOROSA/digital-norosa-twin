import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    ApplicationBuilder, CommandHandler,
    MessageHandler, ContextTypes, filters
)
from agent.builder import build_agent

load_dotenv()

agent = build_agent()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "¡Hola! Soy tu asistente de carrera. Pregúntame cualquier cosa sobre tu perfil."
    )

async def handle_msg(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_msg = update.message.text
    response = agent.chat(user_msg)
    await update.message.reply_text(response)

if __name__ == "__main__":
    app = ApplicationBuilder().token(os.getenv("TELEGRAM_BOT_TOKEN")).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_msg))
    app.run_polling()