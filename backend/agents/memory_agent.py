from core.gpt_fallback import call_gpt
from core.decorator_injector import patch_all_methods
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import os
import pickle


class Memory:
    def __init__(self, dim=384, store_path="data/blueprints/faiss_index.pkl"):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.index = faiss.IndexFlatL2(dim)
        self.texts = []
        self.store_path = store_path
        self.load()

    def add(self, text):
        embedding = self.model.encode([text])
        self.index.add(embedding)
        self.texts.append(text)
        self.save()

    def query(self, text, top_k=3):
        embedding = self.model.encode([text])
        D, I = self.index.search(embedding, top_k)
        return [self.texts[i] for i in I[0] if i < len(self.texts)]

    def save(self):
        os.makedirs(os.path.dirname(self.store_path), exist_ok=True)
        with open(self.store_path, "wb") as f:
            pickle.dump((self.texts, self.index), f)

    def load(self):
        if os.path.exists(self.store_path):
            with open(self.store_path, "rb") as f:
                self.texts, self.index = pickle.load(f)
