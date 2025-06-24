import json
import os
from memory.episodic import EpisodicMemory
from memory.semantic import SemanticMemory

class MemoryStore:
    def __init__(self):
        self.episodic = EpisodicMemory()
        self.semantic = SemanticMemory()

    def retrieve(self, query):
        episodic_results = self.episodic.search(query)
        semantic_summary = self.semantic.retrieve()
        return episodic_results, semantic_summary

    def store(self, user_input, response):
        self.episodic.store(user_input, response)

    def save_to_disk(self, path="data"):
        os.makedirs(path, exist_ok=True)

        
        episodic_data = self.episodic.collection.get()
        with open(os.path.join(path, "episodic_memory.json"), "w") as f:
            json.dump(episodic_data, f, indent=2)

        
        semantic_data = self.semantic.retrieve()
        with open(os.path.join(path, "semantic_memory.txt"), "w") as f:
            f.write(semantic_data)
