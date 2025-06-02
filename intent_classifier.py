from openai import OpenAI
from config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)


def classify_intent(user_prompt: str) -> list[str]:
    system_message = (
        "You are an intent classifier. Based on user input, return a Python list containing any of these strings: "
        "'summarize', 'quiz', 'translate'. If none apply, return an empty list []."
    )

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": f"User input: {user_prompt}"}
        ]
    )

    try:
        actions = eval(response.choices[0].message.content.strip())
        if isinstance(actions, list):
            return actions
    except:
        pass

    return []
