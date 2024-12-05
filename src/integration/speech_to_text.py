import whisper
import ffmpeg

model = whisper.load_model("base")
# tiny, base didn't work in romanian, small, medium, large-2.88GB-8 min, turbo-1.51GB-4 min

async def fetch_transcription(audio_file):
    try:
        result = model.transcribe(audio_file)
        return result["text"]
    except Exception as e:
        print(f"Error transcribing audio: {e}")
        return None

async def ogg_to_wav(audio_ogg_file):
    wav_file = "voice.wav"
    ffmpeg.input(audio_ogg_file).output(wav_file).run()
    return wav_file

