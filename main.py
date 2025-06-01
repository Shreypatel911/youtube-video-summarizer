from fastapi import FastAPI
from pydantic import BaseModel
from downloader import download_audio, compress_audio
from transcriber import transcribe_audio
from summarizer import summarize

app = FastAPI()


class VideoURL(BaseModel):
    url: str


@app.post("/summarize")
def summarize_video(data: VideoURL):
    print("inside main.py")
    audio_mp3 = download_audio(data.url)
    audio_wav = compress_audio(audio_mp3)
    transcript = transcribe_audio(audio_wav)
    result = summarize(transcript)
    return {"summary": result}
