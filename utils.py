import tiktoken


def split_text_by_tokens(text, max_tokens=3000, model="gpt-3.5-turbo"):
    enc = tiktoken.encoding_for_model(model)
    tokens = enc.encode(text)
    chunks = [tokens[i:i+max_tokens]
              for i in range(0, len(tokens), max_tokens)]
    return [enc.decode(chunk) for chunk in chunks]
