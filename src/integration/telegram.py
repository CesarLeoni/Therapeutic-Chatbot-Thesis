from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
from .llm import fetch_response
from dotenv import load_dotenv
import os
import requests
import whisper #speech to text
import ffmpeg #.ogg to .wav

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


# Function to handle voice messages
async def handle_voice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    voice = update.message.voice
    file = await context.bot.get_file(voice.file_id)
    audio_file = "voice.ogg"

    # Download the audio file
    await file.download_to_drive(audio_file)
    print(f"Downloaded audio file to {audio_file}")

    # Convert .ogg to .wav using ffmpeg (since whisper and the pipeline prefer .wav or .mp3)
    # wav_file = "voice.wav"
    # ffmpeg.input(audio_file).output(wav_file).run()

    # Transcribe the audio
    transcription = await process_audio(audio_file)#change here between _ro and basic for romanian
    if transcription:
        response = await fetch_response(transcription)
    else:
        response = "Sorry, I couldn't understand the voice message."

    # Reply with the transcription
    await update.message.reply_text(f"You said: {str(transcription)}\n{str(response)}")

async def process_audio(audio_file):
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

# Main function to initialize the bot
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    # Add handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(MessageHandler(filters.VOICE, handle_voice))  # Add voice handler

    # Start the bot
    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()
