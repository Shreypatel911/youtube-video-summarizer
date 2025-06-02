from openai import OpenAI
from config import OPENAI_API_KEY
from utils import split_text_by_tokens

client = OpenAI(api_key=OPENAI_API_KEY)


def summarize_text(text):
    chunks = split_text_by_tokens(text, max_tokens=3000, model="gpt-4o")
    summaries = []
    print("size of chunks", len(chunks))
    print("first chunk", chunks[0])

    for chunk in chunks:
        prompt = f"Summarize this transcript in bullet points and a short paragraph:\n\n{chunk}"
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that summarizes transcripts."},
                {"role": "user", "content": prompt}
            ]
        )
        summaries.append(response.choices[0].message.content.strip())

    return "\n\n".join(summaries)
