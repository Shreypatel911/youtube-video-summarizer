from yt_dlp import YoutubeDL
import uuid
import os
import subprocess


def download_audio(url: str) -> str:
    file_id = str(uuid.uuid4())
    path = f"audio/{file_id}.mp3"
    ydl_opts = {'format': 'bestaudio/best', 'outtmpl': path}
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    return path


def download_video_file(youtube_url: str) -> str:

    temp_path = os.path.join("temp", f"temp_video_{uuid.uuid4().hex}.mp4")
    final_path = os.path.join("static", f"video_{uuid.uuid4().hex}.mp4")

    os.makedirs("temp", exist_ok=True)
    os.makedirs("static", exist_ok=True)

    ydl_opts = {
        "format": "bestvideo[height<=360]+bestaudio/best[height<=360]",
        "outtmpl": temp_path,
        "quiet": True,
        "merge_output_format": "mp4"
    }

    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([youtube_url])

    # Strip original audio
    command = [
        "ffmpeg",
        "-y",
        "-i", temp_path,
        "-an",  # Remove all audio
        "-c:v", "copy",
        final_path
    ]
    subprocess.run(command, check=True)

    return final_path
