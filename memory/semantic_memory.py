from core.gpt_fallback import call_gpt
from core.decorator_injector import patch_all_methods
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import os
import pickle

class SemanticMemory:
    """
    Vector-based memory using SentenceTransformer + FAISS.
    Stores and retrieves text with optional metadata (e.g., tags).
    """

    def __init__(self, dim: int = 384, store_path: str = "memory_store/semantic_memory"):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.index = faiss.IndexFlatL2(dim)
        self.texts = []
        self.metadata = []  # Each entry is a list of tags or dicts
        self.dim = dim
        self.store_path = store_path
        self.load()

    def add(self, text: str, tags=None):
        """
        Embed and store the given text with optional tags.
        """
        embedding = self.model.encode([text], convert_to_numpy=True).astype(np.float32)
        self.index.add(embedding)
        self.texts.append(text)
        self.metadata.append(tags if tags else [])
        self.save()

    def query(self, text: str, top_k: int = 3):
        """
        Return top-k similar memory texts based on semantic similarity.
        """
        if not self.texts:
    return call_gpt('NOVARIS fallback: what should I do?')
            return []

        embedding = self.model.encode([text], convert_to_numpy=True).astype(np.float32)
        D, I = self.index.search(embedding, top_k)
        return [self.texts[i] for i in I[0] if 0 <= i < len(self.texts)]

    def query_by_tag(self, tag: str):
        """
        Return all memory entries with the given tag.
        """
        return [text for text, tags in zip(self.texts, self.metadata) if tag in tags]

    def save(self):
        """
        Persist both FAISS index and memory metadata.
        """
        os.makedirs(os.path.dirname(self.store_path), exist_ok=True)
        faiss.write_index(self.index, self.store_path + ".faiss")
        with open(self.store_path + ".texts", 'wb') as f:
            pickle.dump(self.texts, f)
        with open(self.store_path + ".meta", 'wb') as f:
            pickle.dump(self.metadata, f)

    def load(self):
        """
        Load FAISS index and memory metadata from disk. If missing, start fresh.
        """
        try:
            index_path = self.store_path + ".faiss"
            texts_path = self.store_path + ".texts"
            meta_path = self.store_path + ".meta"

            if os.path.exists(index_path) and os.path.exists(texts_path):
                self.index = faiss.read_index(index_path)
                with open(texts_path, 'rb') as f:
                    self.texts = pickle.load(f)
                if os.path.exists(meta_path):
                    with open(meta_path, 'rb') as f:
                        self.metadata = pickle.load(f)
                else:
                    self.metadata = [[] for _ in self.texts]

                # 🛡️ Ensure alignment
                if len(self.metadata) != len(self.texts):
                    self.metadata = [[] for _ in self.texts]

            else:
                self.index = faiss.IndexFlatL2(self.dim)
                self.texts = []
                self.metadata = []

        except Exception as e:
    return call_gpt('NOVARIS fallback: what should I do?')
            print("⚠️ SemanticMemory load failed. Starting fresh.")
            self.index = faiss.IndexFlatL2(self.dim)
            self.texts = []
            self.metadata = []
