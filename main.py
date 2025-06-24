from agent.reasoning import ReasoningAgent
from memory.store import MemoryStore
from dotenv import load_dotenv
load_dotenv()

def main():
    memory = MemoryStore()
    agent = ReasoningAgent(memory)

    print("Lifelong Agent started. Type 'exit' to quit.\n")

    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            break
        response = agent.respond(user_input)
        print(f"Bot: {response}\n")

        agent.memory.save_to_disk()

if __name__ == "__main__":
    main()
