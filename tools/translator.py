from openai import OpenAI
from config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)


def translate_text(text: str, target_language="English") -> str:
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system",
                "content": f"Translate the following text to {target_language}."},
            {"role": "user", "content": text}
        ]
    )
    return response.choices[0].message.content.strip()
