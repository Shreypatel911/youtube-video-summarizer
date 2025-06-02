import gradio as gr
from agent import handle_user_input
from tools.quiz import evaluate_quiz

chat_history = []
quiz_id = None
quiz_questions = []
user_answers = []
current_index = 0
in_quiz = False


def render_chat():
    return [(u, a) for u, a in chat_history]


def handle_message(user_input):
    global quiz_id, quiz_questions, user_answers, current_index, in_quiz

    response = handle_user_input(user_input)

    if isinstance(response, dict):
        if "quiz_id" in response:
            in_quiz = True
            quiz_id = response["quiz_id"]
            quiz_questions = response["quiz_questions"]
            user_answers = []
            current_index = 0

            q = quiz_questions[current_index]
            options = [f"{k}. {v}" for k, v in q["options"].items()] if isinstance(
                q["options"], dict) else q["options"]

            chat_history.append(
                (user_input, "🧠 Quiz started. Please answer the questions below.")
            )
            return render_chat(), q["question"], gr.update(choices=options), gr.update(visible=True), "", None, gr.update(visible=False), ""

        if "video_path" in response and "audio_path" in response:
            chat_history.append(
                (user_input, "✅ Video translated and dubbed in English. See below.")
            )
            return render_chat(), "", gr.update(choices=[]), gr.update(visible=False), "", response["video_path"], gr.update(visible=True), ""

    chat_history.append((user_input, response))
    return render_chat(), "", gr.update(choices=[]), gr.update(visible=False), "", None, gr.update(visible=False), ""


def submit_answer(selected):
    global current_index, user_answers, quiz_questions, quiz_id, in_quiz

    if not selected:
        return gr.update(), gr.update(), "⚠️ Please select an answer."

    user_answers.append(selected[0])
    current_index += 1

    if current_index >= len(quiz_questions):
        score, total = evaluate_quiz(quiz_id, user_answers)
        result = f"✅ Quiz Completed! Your score: {score}/{total}"
        chat_history.append(("Quiz", result))
        in_quiz = False
        return "", gr.update(choices=[]), result

    q = quiz_questions[current_index]
    options = [f"{k}. {v}" for k, v in q["options"].items()] if isinstance(
        q["options"], dict) else q["options"]

    return q["question"], gr.update(choices=options), ""


with gr.Blocks() as demo:
    gr.Markdown(
        "## 🧠 YouTube Assistant: Summarize | Quiz | Translate with English Dub")

    chatbot = gr.Chatbot(label="Chat History", height=350)

    with gr.Row():
        user_input = gr.Textbox(
            placeholder="Type your message...", show_label=False)
        send_btn = gr.Button("Send")

    quiz_section = gr.Group(visible=False)
    with quiz_section:
        question_text = gr.Textbox(label="Quiz Question", interactive=False)
        option_radio = gr.Radio(choices=[], label="Choose an answer")
        quiz_feedback = gr.Textbox(label="Score / Warnings", interactive=False)
        next_btn = gr.Button("Next")

    video_section = gr.Group(visible=False)
    with video_section:
        translated_video = gr.Video(label="Dubbed Video")

    send_btn.click(fn=handle_message, inputs=user_input,
                   outputs=[chatbot, question_text, option_radio, quiz_section, quiz_feedback, translated_video, video_section, user_input])

    user_input.submit(fn=handle_message, inputs=user_input,
                      outputs=[chatbot, question_text, option_radio, quiz_section, quiz_feedback, translated_video, video_section, user_input])

    next_btn.click(fn=submit_answer, inputs=[option_radio],
                   outputs=[question_text, option_radio, quiz_feedback])

demo.launch()
