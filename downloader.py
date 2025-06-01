import subprocess
from yt_dlp import YoutubeDL
import os


def download_audio(url, output_file="audio/audio.mp3"):
    ydl_opts = {'format': 'bestaudio/best', 'outtmpl': output_file}
    with YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    return output_file


def compress_audio(input_file="audio/audio.mp3", output_file="audio/audio.wav"):
    print("inside compress_audio")
    cmd = f'ffmpeg -y -i "{input_file}" -ar 16000 -ac 1 -c:a pcm_s16le "{output_file}"'
    subprocess.run(cmd, shell=True, check=True)
    return output_file
