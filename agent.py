from tools.downloader import download_audio, download_video_file
from tools.transcriber import transcribe_audio
from tools.summarizer import summarize_text
from tools.quiz import generate_quiz
from tools.translator import translate_text
from tools.tts import synthesize_audio
from intent_classifier import classify_intent
import re
import uuid
import subprocess

video_cache = {}
session_state = {
    "current_video_id": None,
    "transcript": None,
    "last_quiz_id": None
}


def extract_video_id(url: str) -> str:
    match = re.search(r"(?:v=|youtu\.be/)([\w-]+)", url)
    return match.group(1) if match else None


def extract_youtube_url(text: str) -> str:
    pattern = r"(https?://(?:www\.)?(?:youtube\.com/watch\?v=|youtu\.be/)[\w-]+)"
    match = re.search(pattern, text)
    return match.group(1) if match else None


def extract_num_questions(user_input: str, default: int = 5) -> int:
    match = re.search(r"(\d+)\s*(questions|quiz|qns)?", user_input.lower())
    return int(match.group(1)) if match else default


def merge_video_audio(video_path: str, audio_path: str) -> str:
    output_path = f"static/final_video_{uuid.uuid4().hex}.mp4"
    command = [
        "ffmpeg",
        "-y",
        "-i", video_path,
        "-i", audio_path,
        "-c:v", "copy",
        "-c:a", "aac",
        "-shortest",
        output_path
    ]
    subprocess.run(command, check=True, stderr=subprocess.PIPE,
                   stdout=subprocess.PIPE)
    return output_path


def handle_user_input(user_input: str):
    actions = classify_intent(user_input)

    if not actions:
        return "I'm not sure what you'd like me to do. I can summarize videos, translate or create quizzes from them."

    url = extract_youtube_url(user_input)
    video_id = extract_video_id(url) if url else None

    if not url:
        return "Please provide a YouTube video URL."

    if video_id != session_state["current_video_id"]:
        audio_path = download_audio(url)
        transcript = transcribe_audio(audio_path)
        video_cache[video_id] = {"audio": audio_path, "transcript": transcript}
        session_state["current_video_id"] = video_id
        session_state["transcript"] = transcript
    else:
        transcript = video_cache[video_id]["transcript"]

    if "quiz" in actions:
        num_qs = extract_num_questions(user_input)
        quiz_id, quiz_questions = generate_quiz(
            transcript, num_questions=num_qs)
        session_state["last_quiz_id"] = quiz_id
        return {
            "text": f"🧠 Quiz with {len(quiz_questions)} questions:",
            "quiz_id": quiz_id,
            "quiz_questions": quiz_questions
        }

    if "summarize" in actions:
        summary = summarize_text(transcript)
        return f"🔹 Summary:\n{summary}"

    if "translate" in actions:
        translated = translate_text(transcript, target_language="English")
        audio_path = synthesize_audio(translated)
        video_path = download_video_file(url)
        final_video_path = merge_video_audio(video_path, audio_path)
        return {
            "video_path": final_video_path,
            "audio_path": audio_path
        }

    return "I understood the intent, but nothing to do."
