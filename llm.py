import requests
import time
import os
from dotenv import load_dotenv
load_dotenv()

# 🔐 safer (recommended)

GROQ_API_KEY = os.getenv("API_KEY")

def get_answer(context, question, chat_history=None):
    if not GROQ_API_KEY:
        return "Groq API key is missing. Add API_KEY to your .env file and restart the app."

    url = "https://api.groq.com/openai/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    messages = [
        {
            "role": "system",
            "content": "Answer clearly using only given context. Use bullets if useful."
        },
        {
            "role": "user",
            "content": f"Context: {context}\nQuestion: {question}"
        }
    ]

    data = {
        "model": "llama-3.1-8b-instant",
        "messages": messages,
        "temperature": 0.2,
        "max_tokens": 180,
        "top_p": 0.9
    }

    for attempt in range(3):
        try:
            response = requests.post(
                url,
                headers=headers,
                json=data,
                timeout=25
            )

            # ✅ success
            if response.status_code == 200:
                result = response.json()
                return result["choices"][0]["message"]["content"]

            # 🔁 retry on rate limit
            if response.status_code == 429:
                time.sleep(4 * (attempt + 1))
                continue

            try:
                detail = response.json().get("error", {}).get("message", response.text)
            except ValueError:
                detail = response.text

            return f"API Error {response.status_code}: {detail[:200]}"

        except Exception:
            time.sleep(2)
            continue  # ✅ retry instead of stopping

    return "⚠️ AI is busy. Please try again in a few seconds."
