from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from .llm import fetch_response
from dotenv import load_dotenv
import os

# Load your Telegram bot token from the environment variable
dotenv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
load_dotenv(dotenv_path)

BOT_TOKEN = os.getenv("BOT_TOKEN")

# Handler for the /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Salutare! Eu sunt PsychoBot! Terapeutul si sfătuitorul "
                                    "tău! Cu ce te pot ajuta azi?")

# Handler for user messages
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        user_message = update.message.text
        #await update.message.reply_text("Mă gândesc...")

        # Fetch the response from the LLM
        response = await fetch_response(user_message)
        await update.message.reply_text(response)
    except Exception as e:
        await update.message.reply_text(f"Întâmpin eroarea : {e}")

# Main function to initialize the bot
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Add handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Start the bot
    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
