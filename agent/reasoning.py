import os
import requests
import json

class ReasoningAgent:
    def __init__(self, memory_store):
        self.memory = memory_store
        self.api_key = os.getenv("TOGETHER_API_KEY")
        self.model = "mistralai/Mixtral-8x7B-Instruct-v0.1"  # You can change this

    def respond(self, query):
        # Retrieve relevant memories
        episodic_mem, semantic_context = self.memory.retrieve(query)

        episodic_text = "\n".join([f"User: {m['user']}\nBot: {m['bot']}" for m in episodic_mem])

        prompt = f"""You are a helpful assistant with lifelong memory.

Semantic Knowledge:
{semantic_context}

Episodic Recall:
{episodic_text}

Now answer the new user question:
User: {query}
Bot:"""

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": self.model,
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7
        }

        response = requests.post(
            "https://api.together.xyz/v1/chat/completions",
            headers=headers,
            data=json.dumps(payload)
        )

        if response.status_code != 200:
            raise RuntimeError(f"Together API error: {response.status_code} - {response.text}")

        answer = response.json()["choices"][0]["message"]["content"].strip()

        # Store in episodic memory
        self.memory.store(query, answer)

        return answer
