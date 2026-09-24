import json
import urllib.request
import urllib.error


OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "llama3.2:1b"


def understand_movie_request(user_request):

    prompt = f"""
You are a query rewriting component for an English-language
movie semantic search engine.

The user may write in Turkish or another language.

Your task:
Convert the user's request into ONE concise ENGLISH semantic
movie search query.

STRICT RULES:
- Always output in English.
- Preserve EVERY preference explicitly mentioned by the user.
- Preserve genre, mood, tone, themes, setting and exclusions.
- Translate meaning naturally instead of word-for-word.
- Do not recommend or invent movie titles.
- Do not add ratings, years, actors or preferences that the user
  did not mention.
- Do not use quotation marks.
- Do not explain your answer.
- Output only one search query.

Example:

User:
Sevgilimle izleyebileceğim eğlenceli ama çocukça olmayan
romantik bir film istiyorum

Output:
fun romantic movie for couples with a mature tone, lighthearted
and not childish

User request:
{user_request}

Output:
"""

    request_data = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False
    }

    data = json.dumps(
        request_data
    ).encode("utf-8")

    request = urllib.request.Request(
        OLLAMA_URL,
        data=data,
        headers={
            "Content-Type": "application/json"
        },
        method="POST"
    )

    try:

        with urllib.request.urlopen(
            request,
            timeout=60
        ) as response:

            result = json.loads(
                response.read().decode("utf-8")
            )

        semantic_query = result[
            "response"
        ].strip()

        return {
            "semantic_query": semantic_query,
            "llm_used": True,
            "provider": "ollama",
            "model": OLLAMA_MODEL
        }

    except (
        urllib.error.URLError,
        TimeoutError,
        KeyError,
        json.JSONDecodeError
    ):

        return {
            "semantic_query": user_request,
            "llm_used": False,
            "provider": "fallback"
        }