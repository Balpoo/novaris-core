from core.gpt_fallback import call_gpt
from core.decorator_injector import patch_all_methods

# memory/embedding_store.py

import chromadb
from chromadb.config import Settings
from memory.embedder import Embedder


class EmbeddingStore:
    def __init__(self, collection_name="novaris_memory"):
        self.client = chromadb.Client(Settings(anonymized_telemetry=False))
        self.embedder = Embedder()
        self.collection = self.client.get_or_create_collection(collection_name)

    def add(self, text, metadata=None, id=None):
        embedding = self.embedder.embed(text)[0]
        self.collection.add(
            documents=[text],
            embeddings=[embedding],
            metadatas=[metadata or {}],
            ids=[id or str(hash(text))],
        )

    def query(self, query_text, n_results=5):
        embedding = self.embedder.embed(query_text)[0]
        results = self.collection.query(
            query_embeddings=[embedding], n_results=n_results
        )
        return results
