from openai import OpenAI
from config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)


def summarize_text(text):
    prompt = f"Summarize this transcript in bullet points and a short paragraph:\n\n{text[:4000]}"
    print("text in summarize", text)
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that summarizes transcripts."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content
