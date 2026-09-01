from app.services.retrieval.service import RetrievalService
from app.services.llm.service import LLMService
from .intent import detect_chat_intent
from app.services.paper_lookup.service import PaperLookupService
from app.services.paper_lookup.classifier import detect_requested_section
class ChatService:

    def __init__(self):
        self.retriever = RetrievalService()
        self.llm = LLMService()
        self.lookup = PaperLookupService()

    def ask(
            self,
            question: str,
            paper_ids: list[str],
            history: list = []
    ):
        requested_section = detect_requested_section(question)

        print("REQUESTED SECTION:", requested_section)

        search_query = question

        if not requested_section:
            search_query = self.llm.rewrite_query(
                question,
                history
            )

        print("SEARCH QUERY:", search_query)

        intent = detect_chat_intent(question)

        if intent == "compare":
            answer, results = self.compare_papers(paper_ids)
            suggestions = self.llm.generate_suggestions(question, answer)
            return answer, results, suggestions

        if intent == "literature":
            answer, results = self.generate_literature_review(paper_ids)
            suggestions = self.llm.generate_suggestions(question, answer)
            return answer, results, suggestions

        if intent == "gaps":
            answer, results = self.research_gaps(paper_ids)
            suggestions = self.llm.generate_suggestions(question, answer)
            return answer, results, suggestions

        if requested_section:
            # Previously this only ran when exactly one paper was selected,
            # so any multi-paper question that maps to a specific section
            # (e.g. "who are the authors of these two papers?" -> front_matter)
            # silently fell through to generic vector search, which rarely
            # surfaces front-matter/author text. Now it looks up the section
            # in every selected paper and tags each block with the paper name
            # so the model can tell them apart.
            sections = []

            for paper_id in paper_ids:
                paper_sections = self.lookup.get_sections(
                    paper_id,
                    requested_section
                )

                paper = self.lookup.load_paper(paper_id)
                paper_name = (
                    paper.get("metadata", {}).get("paper_name", paper_id)
                    if paper else paper_id
                )

                for s in paper_sections:
                    s["paper_name"] = paper_name
                    sections.append(s)

            if not sections:
                return (
                    f"I could not find a '{requested_section[0]}' section in the selected paper(s).",
                    [],
                    []
                )

            print("Number of matched sections:", len(sections))

            for s in sections:
                print("->", s["paper_name"], "-", s["heading"])

            context = ""

            for section in sections:
                context += (
                    f"\n\n## {section['paper_name']} — {section['heading']}\n\n"
                    f"{section['content']}"
                )

            answer = self.llm.explain_section(
                question=question,
                section_name=", ".join(
                    f"{s['paper_name']} — {s['heading']}" for s in sections
                ),
                section_text=context
            )

            suggestions = self.llm.generate_suggestions(
                question,
                answer
            )

            return answer, [], suggestions

        results = self.retriever.search(
            query=search_query,
            paper_ids=paper_ids,
            # top_k=5 meant a 2-paper question only got ~2 chunks per paper
            # (top_k // len(paper_ids)) - not enough grounding for anything
            # beyond a trivial single-fact question. Scale with paper count.
            top_k=max(8, 4 * len(paper_ids)) if paper_ids else 8
        )

        answer = self.llm.answer(
            question,   results,   history
        )

        suggestions = self.llm.generate_suggestions(
            question,    answer
        )

        return answer, results, suggestions

    def generate_literature_review(self, paper_ids):

        papers = []

        for paper_id in paper_ids:

            paper = self.lookup.load_paper(paper_id)

            if paper:
                papers.append(paper)

        answer = self.llm.literature_review(papers)

        return answer, []
    def compare_papers(self, paper_ids):

        papers = []

        for paper_id in paper_ids:

            paper = self.lookup.load_paper(paper_id)
            print("=" * 80)
            print("SELECTED PAPER IDS")
            print(paper_ids)
            print("=" * 80)

            if paper:
                papers.append(paper)

        answer = self.llm.compare_papers(papers)

        return answer, []


    def research_gaps(self, paper_ids):

        papers = []

        for paper_id in paper_ids:
            paper = self.lookup.load_paper(paper_id)

            if paper:
                papers.append(paper)

        print("Loaded papers:", len(papers))

        answer = self.llm.research_gaps(papers)

        return answer, []