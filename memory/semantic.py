import openai
import os
from prompts.refine_memory import SEMANTIC_SUMMARY_PROMPT

class SemanticMemory:
    def __init__(self):
        openai.api_key = os.getenv("TOGETHER_API_KEY")
        openai.api_base = "https://api.together.xyz/v1"
        self.knowledge = []

    def summarize(self, memories):
        text = "\n".join([f"User: {m['user']}\nBot: {m['bot']}" for m in memories])
        prompt = SEMANTIC_SUMMARY_PROMPT.format(memory=text)

        response = openai.ChatCompletion.create(
            model="mistralai/Mixtral-8x7B-Instruct-v0.1",
            messages=[{"role": "user", "content": prompt}],
            stream=False
        )
        summary = response["choices"][0]["message"]["content"].strip()
        self.knowledge.append(summary)
        return summary

    def retrieve(self):
        return "\n".join(self.knowledge)
