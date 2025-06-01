from openai import OpenAI
from config import OPENAI_API_KEY
from tools.compresser import compress_audio

client = OpenAI(api_key=OPENAI_API_KEY)


def transcribe_audio(audio_path: str) -> str:
    wav_path = compress_audio(audio_path)
    with open(wav_path, "rb") as f:
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=f
        )
    return transcript.text
