from openai import OpenAI
import uuid
import os
from config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)


def synthesize_audio(text: str) -> str:
    output_dir = "audio"
    os.makedirs(output_dir, exist_ok=True)

    filename = os.path.join(output_dir, f"audio_{uuid.uuid4().hex}.mp3")
    response = client.audio.speech.create(
        model="tts-1",
        voice="nova",
        input=text
    )
    with open(filename, "wb") as f:
        f.write(response.content)
    return filename
