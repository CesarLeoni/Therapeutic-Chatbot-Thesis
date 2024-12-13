from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from src.integration.llm import fetch_response
from dotenv import load_dotenv
from src.integration.speech_to_text import fetch_transcription
from telegram.error import Conflict
from src.conf.logger import get_logger
import os
import asyncio

logger = get_logger(__name__)  # Set up the logger

# Load your Telegram bot token from the environment variable
dotenv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
load_dotenv(dotenv_path)
BOT_TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.info("Bot received a /start command")
    await update.message.reply_text("Salutare! Eu sunt PsychoBot! Terapeutul și sfătuitorul tău! Cu ce te pot ajuta azi?")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        user_message = update.message.text
        logger.info(f"Received message: {user_message}")
        await update.message.reply_text("Mă gândesc...")

        response = await fetch_response(user_message)
        logger.debug(f"Generated response: {response}")
        await update.message.reply_text(response)
    except Exception as e:
        logger.error(f"Error handling message: {e}", exc_info=True)
        await update.message.reply_text(f"Întâmpin eroarea : {e}")

async def handle_voice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        voice = update.message.voice
        file = await context.bot.get_file(voice.file_id)
        audio_file = "voice.ogg"

        await file.download_to_drive(audio_file)
        logger.info(f"Downloaded audio file to {audio_file}")

        await update.message.reply_text("Mă gândesc...")
        transcription = await fetch_transcription(audio_file)
        response = await fetch_response(transcription or "Voice not understood.")
        logger.debug(f"Transcription: {transcription}, Response: {response}")

        await update.message.reply_text(f"You said: {str(transcription)}\n{str(response)}")
    except Exception as e:
        logger.error(f"Error handling voice message: {e}", exc_info=True)
        await update.message.reply_text("An error occurred while processing your voice message.")

async def error_handler(update, context):
    if isinstance(context.error, Conflict):
        logger.warning("Conflict error: Ensure only one bot instance is running.")
    else:
        logger.error(f"An error occurred: {context.error}", exc_info=True)

def main():
    logger.info("Initializing the bot")
    app = ApplicationBuilder().token(BOT_TOKEN).concurrent_updates(True).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(MessageHandler(filters.VOICE, handle_voice))
    app.add_error_handler(error_handler)

    logger.info("Bot is running...")
    print("Bot is running...")
    app.run_polling(poll_interval=1.0, timeout=30, read_timeout=30)

if __name__ == "__main__":
    main()
