from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from .llm import fetch_response
from dotenv import load_dotenv
import os
import requests
import whisper #speech to text
import ffmpeg #.ogg to .wav
import asyncio
import concurrent.futures

#from transformers import pipeline
#pipe = pipeline("automatic-speech-recognition", model="gigant/whisper-medium-romanian")



# Load your Telegram bot token from the environment variable
dotenv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
load_dotenv(dotenv_path)

BOT_TOKEN = os.getenv("BOT_TOKEN")

# Handler for the /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Salutare! Eu sunt PsychoBot! Terapeutul si sfătuitorul "
                                    "tău! Cu ce te pot ajuta azi?")
    print(update.message)

# Handler for user messages
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        user_message = update.message.text
        #await update.message.reply_text("Mă gândesc...")

        # Fetch the response from the LLM
        response = await fetch_response(user_message)
        await update.message.reply_text(response)
        print(f"user: {user_message}\nresponse: {response}")
        print(update.message)
    except Exception as e:
        await update.message.reply_text(f"Întâmpin eroarea : {e}")


# Function to handle voice messages
async def handle_voice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        voice = update.message.voice
        file = await context.bot.get_file(voice.file_id)
        audio_file = "voice.ogg"

        # Download the audio file
        await file.download_to_drive(audio_file)
        print(f"Downloaded audio file to {audio_file}")

        await update.message.reply_text("Mă gândesc...")

        # Convert .ogg to .wav using ffmpeg (since whisper and the pipeline prefer .wav or .mp3)
        # wav_file = "voice.wav"
        # ffmpeg.input(audio_file).output(wav_file).run()

        # Run transcription asynchronously
        #transcription_task = asyncio.create_task(process_audio("voice.ogg"))
        #transcription = await transcription_task

        with concurrent.futures.ThreadPoolExecutor() as pool:
            transcription = await asyncio.get_event_loop().run_in_executor(pool, process_audio, audio_file)

        # Transcribe the audio
        # transcription = await process_audio(audio_file)
        # change here between _ro and basic for romanian
        response = await fetch_response(transcription or "Voice not understood.")

        # Reply with the transcription
        await update.message.reply_text(f"You said: {str(transcription)}\n{str(response)}")
    except Exception as e:
        print(f"Error handling voice message: {e}")
        await update.message.reply_text("An error occurred while processing your voice message.")


def process_audio(audio_file):
    try:
        model = whisper.load_model("base")
        result = model.transcribe(audio_file)
        return result["text"]
    except Exception as e:
        print(f"Error transcribing audio: {e}")
        return None

# # Function to process audio using the transformers pipeline
# async def process_audio_ro(audio_file):
#     try:
#         # Use the pipeline to transcribe the audio
#         transcription = pipe(audio_file)
#         return transcription["text"]
#     except Exception as e:
#         print(f"Error transcribing audio: {e}")
#         return None

from telegram.error import Conflict

async def error_handler(update, context):
    if isinstance(context.error, Conflict):
        print("Conflict error: Ensure only one bot instance is running.")
    else:
        print(f"An error occurred: {context.error}")


# Main function to initialize the bot
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).concurrent_updates(True).build()

    # Add handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(MessageHandler(filters.VOICE, handle_voice))  # Add voice handler
    app.add_error_handler(error_handler)

    # Start polling with increased worker pool and larger timeout
    print("Bot is running...")
    app.run_polling(poll_interval=1.0, timeout=30, read_timeout=30)

if __name__ == "__main__":
    main()
