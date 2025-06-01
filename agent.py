from tools.downloader import download_audio
from tools.transcriber import transcribe_audio
from tools.summarizer import summarize_text
from tools.quiz import generate_quiz
from intent_classifier import classify_intent
import re

# 🔁 Memory across user prompts
memory = {
    "video_id": None,
    "transcript": None,
    "last_summary": None,
    "last_quiz": None
}

video_cache = {}


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


def handle_user_input(user_input: str):
    actions = classify_intent(user_input)

    if not actions:
        return "I can summarize YouTube videos or create quizzes from them. Please clarify what you'd like me to do."

    url = extract_youtube_url(user_input)
    video_id = extract_video_id(url) if url else None

    if video_id:
        if video_id in video_cache:
            print(f"🔁 Using cached transcript for video: {video_id}")
            transcript = video_cache[video_id]["transcript"]
        else:
            print(f"⬇️ Downloading and transcribing new video: {video_id}")
            audio = download_audio(url)
            transcript = transcribe_audio(audio)
            video_cache[video_id] = {"audio": audio, "transcript": transcript}

        # Store in memory
        memory["video_id"] = video_id
        memory["transcript"] = transcript

    elif memory["transcript"]:
        print(
            f"🧠 Using remembered transcript from video: {memory['video_id']}")
        transcript = memory["transcript"]
    else:
        return "Please provide a YouTube video link to begin."

    response_parts = []

    if "summarize" in actions:
        summary = summarize_text(transcript)
        memory["last_summary"] = summary
        response_parts.append("🔹 Summary:\n" + summary)

    if "quiz" in actions:
        num_qs = extract_num_questions(user_input)
        quiz = generate_quiz(transcript, num_questions=num_qs)
        memory["last_quiz"] = quiz
        response_parts.append("🧠 Quiz:\n" + quiz)

    return "\n\n".join(response_parts) if response_parts else "I understood your intent but have no action to perform."


if __name__ == "__main__":
    print("💬 YouTube Agent Ready. Type 'exit' to quit.")
    while True:
        user_prompt = input("You: ")
        if user_prompt.lower() in {"exit", "quit"}:
            break
        response = handle_user_input(user_prompt)
        print("\nAgent:\n" + response + "\n")
