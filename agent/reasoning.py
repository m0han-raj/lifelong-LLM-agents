import openai
import os

class ReasoningAgent:
    def __init__(self, memory_store):
        self.memory = memory_store

        
        openai.api_key = os.getenv("TOGETHER_API_KEY")
        openai.api_base = "https://api.together.xyz/v1"  

    def respond(self, query):
        
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

        
        response = openai.ChatCompletion.create(
            model="mistralai/Mixtral-8x7B-Instruct-v0.1",  
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            stream=False
        )

        answer = response["choices"][0]["message"]["content"].strip()

        
        self.memory.store(query, answer)

        return answer
