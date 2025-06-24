from memory.episodic import EpisodicMemory
from memory.semantic import SemanticMemory

class MemoryStore:
    def __init__(self):
        self.episodic = EpisodicMemory()
        self.semantic = SemanticMemory()

    def store(self, query, response):
        self.episodic.store(query, response)

    def retrieve(self, query):
        episodic_mem = self.episodic.search(query)
        semantic_context = self.semantic.retrieve()
        return episodic_mem, semantic_context
