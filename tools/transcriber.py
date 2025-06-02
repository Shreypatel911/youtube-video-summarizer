from openai import OpenAI
from config import OPENAI_API_KEY
from tools.compresser import compress_audio
from pydub import AudioSegment
import os

client = OpenAI(api_key=OPENAI_API_KEY)


def split_audio(audio_path, chunk_ms=5 * 60 * 1000):
    audio = AudioSegment.from_file(audio_path)
    chunks = []
    for i in range(0, len(audio), chunk_ms):
        chunk = audio[i:i+chunk_ms]
        chunk_path = f"{audio_path}_chunk_{i//chunk_ms}.wav"
        chunk.export(chunk_path, format="wav")
        chunks.append(chunk_path)
    return chunks


def transcribe_audio(audio_path: str) -> str:
    wav_path = compress_audio(audio_path)
    chunks = split_audio(wav_path)

    full_text = ""
    for chunk_path in chunks:
        with open(chunk_path, "rb") as f:
            response = client.audio.transcriptions.create(
                model="whisper-1",
                file=f
            )
            full_text += response.text + "\n"

    return full_text.strip()
