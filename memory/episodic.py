import chromadb
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction

class EpisodicMemory:
    def __init__(self, persist_dir="data/chroma", collection_name="episodic_memory"):
        self.client = chromadb.PersistentClient(path=persist_dir)

        embed_fn = SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")  # type: ignore

        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            embedding_function=embed_fn
        )

        self.count = len(self.collection.get()["ids"])

    def store(self, user_input, response):
        doc_id = f"id_{self.count}"
        self.collection.add(
            ids=[doc_id],
            documents=[f"User: {user_input}\nBot: {response}"],
            metadatas=[{"user": user_input, "bot": response}]
        )
        self.count += 1

    def search(self, query, k=3):
        results = self.collection.query(query_texts=[query], n_results=k)
        return [r for r in results['metadatas'][0]]
