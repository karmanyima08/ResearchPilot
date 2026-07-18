from app.services.retrieval.service import RetrievalService
from app.services.llm.service import LLMService
class ChatService:

    def __init__(self):
        self.retriever = RetrievalService()
        self.llm = LLMService()

    def ask(
            self,
            question: str,
            paper_ids: list[str],
            history: list = []
    ):
        search_query = self.llm.rewrite_query(
            question,
            history
        )

        print("SEARCH QUERY:", search_query)

        results = self.retriever.search(
            query=search_query,
            paper_ids=paper_ids,
            top_k=5
        )

        answer = self.llm.answer(
            question,   results,   history
        )

        suggestions = self.llm.generate_suggestions(
            question,    answer
        )

        return answer, results, suggestions

    def generate_literature_review(
        self,
        paper_ids: list[str]
    ):

        results = self.retriever.search(
            query="summarize compare contributions limitations",
            paper_ids=paper_ids,
            top_k=10
        )

        answer = self.llm.literature_review(results)

        return answer, results

    def compare_papers(
            self,
            paper_ids: list[str]
    ):
        results = self.retriever.search(
            query="main contributions methodology strengths weaknesses comparison",
            paper_ids=paper_ids,
            top_k=12
        )

        answer = self.llm.compare_papers(results)

        return answer, results

    def research_gaps(self, paper_ids):
        results = self.retriever.search(
            query="limitations research gaps future work",
            paper_ids=paper_ids,
            top_k=12
        )

        answer = self.llm.research_gaps(results)

        return answer, results