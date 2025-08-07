import os
import json
from openai import OpenAI
import time

# Load OpenAI API key from environment variable
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
assert OPENAI_API_KEY, "Please set your OPENAI_API_KEY environment variable."
client = OpenAI(api_key=OPENAI_API_KEY)

LETTERS_PATH = "data/letters.json"
EMBEDDINGS_PATH = "data/letter_embeddings.json"

with open(LETTERS_PATH, "r", encoding="utf-8") as f:
    letters = json.load(f)

embeddings = []
for idx, letter in enumerate(letters):
    text = letter.get("text", "")
    if text is None or not str(text).strip():
        embeddings.append(None)
        continue
    try:
        response = client.embeddings.create(
            model="text-embedding-3-small",
            input=text
        )
        emb = response.data[0].embedding
        embeddings.append(emb)
    except Exception as e:
        print(f"Error for letter {idx}: {e}")
        embeddings.append(None)
    time.sleep(0.5)  # avoid rate limits

# Save embeddings alongside letter metadata
output = []
for letter, emb in zip(letters, embeddings):
    item = dict(letter)
    item["embedding"] = emb
    output.append(item)

with open(EMBEDDINGS_PATH, "w", encoding="utf-8") as f:
    json.dump(output, f, ensure_ascii=False, indent=2)

print(f"Saved {len(output)} embeddings to {EMBEDDINGS_PATH}")
