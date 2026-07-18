from .models import SearchResult
from app.services.embeddings.service import EmbeddingService
from app.services.vector_store.service import VectorStoreService
class RetrievalService:

    def __init__(self):
        self.embedding = EmbeddingService()
        self.vector_store = VectorStoreService()

    def search(
            self,
            query: str,
            paper_ids: list[str] | None = None,
            top_k: int = 5
    ):
        query_embedding = self.embedding.model.encode([query])[0]

        query_kwargs = {
            "query_embeddings": [query_embedding.tolist()],
            "n_results": top_k
        }

        if paper_ids:

            all_results = []

            for paper_id in paper_ids:

                kwargs = {
                    "query_embeddings": [query_embedding.tolist()],
                    "n_results": top_k,
                    "where": {
                        "paper_id": paper_id
                    }
                }

                results = self.vector_store.db.collection.query(
                    **kwargs
                )

                for i in range(len(results["documents"][0])):
                    all_results.append(
                        SearchResult(
                            content=results["documents"][0][i],
                            score=results["distances"][0][i],
                            metadata=results["metadatas"][0][i]
                        )
                    )
            all_results.sort(
                key=lambda x: x.score
            )

            return all_results[:top_k]
        results = self.vector_store.db.collection.query(
            **query_kwargs
        )

        print("QUERY KWARGS:")
        print(query_kwargs)
        retrieved = []

        print("\nRESULTS:")
        print(results)

        for i in range(len(results["documents"][0])):

            retrieved.append(
                SearchResult(
                    content=results["documents"][0][i],
                    score=results["distances"][0][i],
                    metadata=results["metadatas"][0][i]
                )
            )

        return retrieved