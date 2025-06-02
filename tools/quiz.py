from openai import OpenAI
from config import OPENAI_API_KEY
import json
import uuid
import re

client = OpenAI(api_key=OPENAI_API_KEY)

answer_keys = {}


def clean_json_block(raw):
    # Remove ```json or ``` if present
    cleaned = re.sub(r"^```json", "", raw.strip(), flags=re.IGNORECASE)
    cleaned = re.sub(r"^```", "", cleaned.strip())
    cleaned = re.sub(r"```$", "", cleaned.strip())
    return cleaned.strip()


def generate_quiz(text, num_questions=5):
    prompt = f"""
    Generate {num_questions} multiple-choice questions (MCQs) from the transcript below. Each question must include:
    - A question
    - 4 options labeled A, B, C, D
    - Correct answer letter

    Format: JSON list with 'question', 'options', and 'answer'.

    Transcript:
    {text[:4000]}
    """

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}]
    )

    quiz_raw = response.choices[0].message.content.strip()
    cleaned = clean_json_block(quiz_raw)
    print("quiz returned from LLM: ", quiz_raw)
    print("quiz returned from LLM: ", cleaned)
    quiz_data = json.loads(cleaned)

    quiz_id = str(uuid.uuid4())
    answer_keys[quiz_id] = {i: q["answer"] for i, q in enumerate(quiz_data)}

    user_quiz = [{"question": q["question"], "options": q["options"]}
                 for q in quiz_data]
    return quiz_id, user_quiz


def evaluate_quiz(quiz_id, user_answers):
    correct_answers = answer_keys.get(quiz_id, {})
    score = sum(
        1 for i, ans in enumerate(user_answers)
        if ans.upper() == correct_answers.get(i, "")
    )
    return score, len(correct_answers)
