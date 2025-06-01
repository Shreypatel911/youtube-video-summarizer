from openai import OpenAI
from config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)


def generate_quiz(text, num_questions=5):
    prompt = f"""
    Generate {num_questions} multiple-choice questions (MCQs) from the transcript below. Each question must include:
    - A question
    - 4 options labeled A, B, C, D
    - Correct answer letter
    Format: JSON list with fields 'question', 'options', and 'answer'.

    Transcript:
    {text[:4000]}
    """

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content.strip()
