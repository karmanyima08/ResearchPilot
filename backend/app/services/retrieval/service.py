from .models import SearchResult
from app.services.embeddings.service import EmbeddingService
from app.services.vector_store.service import VectorStoreService


class RetrievalService:

    def __init__(self):
        self.embedding = EmbeddingService()
        self.vector_store = VectorStoreService()

    def search(self, query: str, top_k: int = 5):

        query_embedding = self.embedding.model.encode([query])[0]

        results = self.vector_store.db.collection.query(
            query_embeddings=[query_embedding.tolist()],
            n_results=top_k
        )

        retrieved = []

        for i in range(len(results["documents"][0])):

            retrieved.append(
                SearchResult(
                    content=results["documents"][0][i],
                    score=results["distances"][0][i],
                    metadata=results["metadatas"][0][i]
                )
            )

        return retrieved