import subprocess
import os


def compress_audio(input_path: str) -> str:
    output_path = input_path.replace(".mp3", ".wav")
    cmd = f'ffmpeg -y -i "{input_path}" -ar 16000 -ac 1 -c:a pcm_s16le "{output_path}"'
    subprocess.run(cmd, shell=True, check=True)
    return output_path
