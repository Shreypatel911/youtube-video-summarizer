from yt_dlp import YoutubeDL
import uuid


def download_audio(url: str) -> str:
    file_id = str(uuid.uuid4())
    path = f"audio/{file_id}.mp3"
    ydl_opts = {'format': 'bestaudio/best', 'outtmpl': path}
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    return path
