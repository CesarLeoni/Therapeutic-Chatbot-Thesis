import whisper
import ffmpeg
from conf.logger import get_logger

logger = get_logger(__name__)

model = whisper.load_model("base")

async def fetch_transcription(audio_file):
    try:
        logger.info(f"Starting transcription for {audio_file}")
        result = model.transcribe(audio_file)
        logger.debug(f"Transcription result: {result['text']}")
        return result["text"]
    except Exception as e:
        logger.error(f"Error transcribing audio: {e}", exc_info=True)
        return None

async def ogg_to_wav(audio_ogg_file):
    try:
        logger.info(f"Converting {audio_ogg_file} to WAV format")
        wav_file = "voice.wav"
        ffmpeg.input(audio_ogg_file).output(wav_file).run()
        logger.info(f"Conversion complete: {wav_file}")
        return wav_file
    except Exception as e:
        logger.error(f"Error converting {audio_ogg_file} to WAV: {e}", exc_info=True)
        return None
