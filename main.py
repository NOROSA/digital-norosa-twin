import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)
from agent.builder import chat_sync

load_dotenv()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "¡Hola! Soy el asistente de Norbert. Pregúntame cualquier cosa sobre su trayectoria profesional, proyectos y logros."
    )

async def handle_msg(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_msg = update.message.text
    response = chat_sync(user_msg)
    await update.message.reply_text(response)

if __name__ == "__main__":
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    app = ApplicationBuilder().token(token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_msg))

    app.run_polling()