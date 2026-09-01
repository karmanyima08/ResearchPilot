from .models import SearchResult
from app.services.embeddings.service import EmbeddingService
from app.services.vector_store.service import VectorStoreService

METHOD_SECTIONS = [
    "method",
    "methods",
    "methodology",
    "approach",
    "framework",
    "pipeline",
    "training",
    "implementation",
    "model",
    "models"
]
RESULT_SECTIONS = [
    "result",
    "results",
    "analysis",
    "finding",
    "findings",
    "experiment",
    "experiments",
    "evaluation",
    "benchmark"
]

DISCUSSION_SECTIONS = [
    "discussion",
    "limitation",
    "limitations",
    "future work",
    "future directions",
    "conclusion"
]
class RetrievalService:

    def __init__(self):
        self.embedding = EmbeddingService()
        self.vector_store = VectorStoreService()

    def detect_section_filter(self, query: str):
        query = query.lower()

        if any(word in query for word in METHOD_SECTIONS):
            return METHOD_SECTIONS

        if any(word in query for word in RESULT_SECTIONS):
            return RESULT_SECTIONS

        if any(word in query for word in DISCUSSION_SECTIONS):
            return DISCUSSION_SECTIONS

        return None

    def search(
            self,
            query: str,
            paper_ids: list[str] | None = None,
            top_k: int = 5
    ):
        query_embedding = self.embedding.model.encode([query])[0]
        section_filter = None

        query_kwargs = {
            "query_embeddings": [query_embedding.tolist()],
            "n_results": top_k
        }

        if paper_ids:

            all_results = []

            # Get an equal number of chunks from each selected paper.
            # Floor division here used to leave only 1-2 chunks per paper
            # for any multi-paper question, starving synthesis questions
            # (compare/gaps/authors) of context. Guarantee a reasonable
            # minimum per paper regardless of top_k.
            chunks_per_paper = max(4, top_k // len(paper_ids))

            for paper_id in paper_ids:

                kwargs = {
                    "query_embeddings": [query_embedding.tolist()],
                    "n_results": chunks_per_paper,
                    "where": {
                        "paper_id": paper_id
                    }
                }

                results = self.vector_store.db.collection.query(**kwargs)

                for i in range(len(results["documents"][0])):

                    metadata = results["metadatas"][0][i]

                    if section_filter:
                        heading = metadata.get("heading", "").lower()

                        if not any(s in heading for s in section_filter):
                            continue

                    all_results.append(
                        SearchResult(
                            content=results["documents"][0][i],
                            score=results["distances"][0][i],
                            metadata=metadata
                        )
                    )

            all_results.sort(key=lambda x: x.score)

            return all_results
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