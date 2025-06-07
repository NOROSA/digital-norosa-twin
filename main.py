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
from agent.builder import chat_async

load_dotenv()  # Variables locales

# ──────────────────────────────
# Handlers de Telegram
# ──────────────────────────────
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "¡Hola! Soy el asistente de Norbert Rodríguez. "
        "Pregúntame cualquier cosa sobre su trayectoria profesional, proyectos y logros."
    )


async def handle_msg(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_msg = update.message.text
    response = await chat_async(user_msg)  # ← llamada asíncrona
    await update.message.reply_text(response)


# ──────────────────────────────
# Bootstrap del bot
# ──────────────────────────────
if __name__ == "__main__":
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        raise RuntimeError("Variable TELEGRAM_BOT_TOKEN no definida")

    app = ApplicationBuilder().token(token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_msg))

    # evita conflictos si se relanza mientras otro contenedor está activo
    app.run_polling(drop_pending_updates=True)
