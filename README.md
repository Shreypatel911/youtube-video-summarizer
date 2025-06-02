# YouTube Assistant — Summarize | Quiz | Translate with English Dub

This AI-powered YouTube Assistant enables users to **summarize**, **generate quizzes**, and **translate+dub videos into English**, all through a conversational interface. Just paste a YouTube URL and ask for what you want — no manual video or audio processing required.

---

## Features

- **Summarization**: Get bullet-point and paragraph summaries of video transcripts.
- **Quiz Generator**: Automatically generate MCQs from YouTube video content.
- **Translation & Dubbing**: Translate foreign-language videos into English and dub them with synthetic voice-over.
- **Video Rendering**: Merges the dubbed English audio with a stripped-down low-res (360p) version of the original video.

---

## Technologies & Frameworks Used

- **LangChain (design pattern only)**
- **OpenAI API**
  - `gpt-4o` for summarization, translation, quiz generation
  - `tts-1` for text-to-speech dubbing
  - `whisper-1` for transcription
- **Gradio** – UI interface
- **yt-dlp** – for audio/video downloading
- **ffmpeg** – for media manipulation (strip/mix audio, convert formats)
- **Python Libraries**:
  - `pydub`, `uuid`, `re`, `json`, `subprocess`, `os`
  - `tiktoken` – token-based text splitting

---

## ▶How to Run / Test

### Prerequisites

- Python 3.8+
- FFmpeg installed and accessible via terminal (`ffmpeg` command)
- OpenAI API Key (add to `config.py` as `OPENAI_API_KEY = "your-key"`)

### 📦 Install Dependencies

command to download all packages
pip install -r requirements.txt

requirements.txt should contain

openai
yt-dlp
pydub
tiktoken
gradio

To launch the app run the command - 
python ui.py

Then open the generated Gradio UI in your browser. Paste a YouTube video URL and type prompts like:

"Summarize this video"
"Give me a quiz of 3 questions"
"Translate and dub this video in English"

Future improvements

- This is more efficient with youtube videos which are more audio heavy and have less visuals
- So future enhancements can be made with visuals as well
