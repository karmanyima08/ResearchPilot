from .client import GroqClient
from .prompts import SYSTEM_PROMPT

# NOTE: llama-3.1-8b-instant and llama-3.3-70b-versatile are deprecated on
# Groq (shutdown Aug 16, 2026) - use their recommended replacements instead.
# gpt-oss-20b is small/fast but too shallow for real synthesis - it produces
# generic, repetitive, template-y writing on anything that requires actually
# reasoning across multiple chunks/papers (answers, comparisons, lit reviews,
# gap analysis). Use the larger model for those. Keep the small/fast model
# only for trivial, low-stakes calls like generating follow-up questions,
# where speed matters more than depth.
QUALITY_MODEL = "openai/gpt-oss-120b"
FAST_MODEL = "openai/gpt-oss-20b"


class LLMService:

    def __init__(self):
        self.client = GroqClient().client

    def rewrite_query(self, question, history):
        """
        Resolve pronouns/references ("it", "this method", "they"...) against
        recent conversation history so retrieval actually searches for the
        right thing, not just the literal current question. Previously this
        was a no-op, which meant the system prompt's instruction to resolve
        such references was decorative - retrieval never saw the resolved
        query.
        """
        if not history:
            return question

        history_text = ""
        for msg in history[-6:]:
            role = msg.role.capitalize() if hasattr(msg, "role") else msg["role"].capitalize()
            content = msg.content if hasattr(msg, "content") else msg["content"]
            history_text += f"{role}: {content}\n"

        prompt = f"""Given this conversation history:

{history_text}

Rewrite the following follow-up question into a fully self-contained
search query by resolving any pronouns or references (it, they, this,
that, these, those, the method, the model, etc.) using the history.

If the question is already self-contained, return it unchanged.

Follow-up question: {question}

Return ONLY the rewritten query, nothing else."""

        completion = self.client.chat.completions.create(
            model=FAST_MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
        )

        rewritten = completion.choices[0].message.content.strip()
        return rewritten or question

    def answer(self, question, search_results, history=[]):
        from collections import defaultdict
        paper_chunks = defaultdict(list)
        for result in search_results:

            if isinstance(result, dict):
                metadata = result["metadata"]
                content = result["content"]
            else:
                metadata = result.metadata
                content = result.content

            paper_name = metadata.get("paper_name", "Unknown Paper")

            # 1200 chars per chunk was starving the model of context on
            # synthesis-heavy questions. Chunks are ~1000 chars at ingestion
            # time anyway, so this limit should rarely need to truncate.
            paper_chunks[paper_name].append(content[:2500])

        context = ""
        for paper_name, chunks in paper_chunks.items():
            context += f"\n\n========== {paper_name} ==========\n\n"
            for chunk in chunks:
                context += chunk + "\n\n"

        if not context.strip():
            context = "(No relevant passages were retrieved.)"

        prompt = f"""Retrieved context:
{context}

Question: {question}

Answer the question directly using only the context above. Choose
whatever structure best fits this specific question - plain prose for a
simple factual question, a short explanation with a couple of relevant
subpoints for a conceptual question, a table for a comparison, etc. Don't
default to a fixed template.

Attribute facts naturally to the paper they came from as you write,
rather than tagging every sentence with a mechanical "(Source: ...)".

If the context doesn't contain the answer, say so directly - don't
speculate or fill in with outside knowledge.

Only mention a "simpler explanation" if the material is genuinely
technical or the user asked for one - don't add it by default."""

        messages = [
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            }
        ]

        for msg in history[-6:]:
            messages.append(
                {
                    "role": msg.role if hasattr(msg, "role") else msg["role"],
                    "content": msg.content if hasattr(msg, "content") else msg["content"]
                }
            )

        messages.append(
            {
                "role": "user",
                "content": prompt
            }
        )
        completion = self.client.chat.completions.create(

            model=QUALITY_MODEL,

            messages=messages,

            temperature=0.2

        )
        return completion.choices[0].message.content

    def explain_section(
            self,
            question: str,
            section_name: str,
            section_text: str
    ):

        prompt = f"""
        You are ResearchPilot.

        The user asked:

        {question}

        The following text is the "{section_name}" section of a research paper.

        Rules:

        1. Answer ONLY using this section - no outside knowledge.
        2. Always explain and synthesize in your own words - never paste
           large blocks of the source text verbatim, even for "what is..."
           or "show me..." questions. A real explanation of the content is
           more useful than a copy of it.
        3. Skip anything irrelevant to the question - author names,
           affiliations, emails, and other front-matter noise that happens
           to be adjacent to the requested section should not appear in
           your answer unless the question is specifically about authors.
        4. "Summarize..." -> give a concise summary, not a full explanation.
        5. Do NOT generate takeaways or extra sections unless explicitly asked.
        6. Do NOT mention information from other sections.
        7. If the question asks about something like authors across multiple
           papers, clearly distinguish which paper each fact belongs to
           using the paper names given in the section headers below.

        Section(s):

        {section_text[:8000]}
        """

        response = self.client.chat.completions.create(

            model=QUALITY_MODEL,

            messages=[
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],

            temperature=0

        )

        return response.choices[0].message.content

    def generate_suggestions(
            self,
            question: str,
            answer: str
    ):
        prompt = f"""
    You are generating follow-up questions.

    Original Question:
    {question}

    Answer:
    {answer}

    Generate exactly 4 useful follow-up questions.

    Rules:
    - Continue naturally from the answer.
    - Maximum 8 words.
    - One question per line.
    - No numbering.
    - No bullet points.
    - No blank lines.
    - Only output the questions.
    """
        completion = self.client.chat.completions.create(

            model=FAST_MODEL,

            messages=[
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],

            temperature=0.3

        )
        suggestions = [
            line.strip()
            for line in completion.choices[0].message.content.split("\n")
            if line.strip()
        ]

        return suggestions[:4]

    def literature_review(self, papers):

        context = self.build_papers_context(papers)

        prompt = f"""
        You are ResearchPilot.

        You are writing a scholarly literature review based ONLY on the selected papers.

        ====================================================
        SELECTED PAPERS
        ====================================================

        {context}

        ====================================================

        Rules

        - Use ONLY the selected papers.
        - Never use outside knowledge.
        - Never invent authors, papers, datasets or methods.
        - Do NOT summarize papers one by one.
        - Instead, synthesize the literature across papers.
        - If only one paper discusses a topic, state that explicitly.
        - Every factual statement must end with:
        (Source: Paper → Section)

        ====================================================

        # Introduction

        Briefly describe the common research domain and why it is important.

        ----------------------------------------------------

        # Research Themes

        Identify the major themes emerging across the selected papers.

        For EACH theme:

        • Theme name

        • Which papers belong

        • Main idea

        • Similarities

        • Differences

        Do NOT create themes unsupported by the papers.

        ----------------------------------------------------

        # Methodological Trends

        Compare methodologies across papers.

        Discuss

        • frameworks

        • architectures

        • retrieval methods

        • training strategies

        • evaluation strategies

        Focus on comparison rather than description.

        ----------------------------------------------------

        # Comparative Analysis

        Discuss

        • where papers agree

        • where papers differ

        • strengths of different approaches

        • weaknesses of different approaches

        ----------------------------------------------------

        # Current State of Research

        Explain what has already been achieved collectively.

        Avoid repeating individual paper summaries.

        ----------------------------------------------------

        # Remaining Challenges

        Only include challenges explicitly discussed or clearly implied by comparing multiple papers.

        Do NOT invent challenges.

        ----------------------------------------------------

        # Future Research Directions

        Merge future work suggested across papers.

        Remove duplicate ideas.

        Explain which directions appear most promising.

        ----------------------------------------------------

        # Conclusion

        Write one analytical paragraph summarizing the overall progress of this research area.

        Do NOT simply list papers.
        Do NOT repeat previous sections.
        """

        completion = self.client.chat.completions.create(
            model=QUALITY_MODEL,
            messages=[
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.2
        )

        return completion.choices[0].message.content

    def build_papers_context(self, papers):

        IMPORTANT_SECTIONS = [
            "abstract",
            "introduction",
            "method",
            "methods",
            "methodology",
            "experiment",
            "experiments",
            "results",
            "limitations",
            "future_work",
            "future work",
            "conclusion",
        ]

        SECTION_LIMIT = 700

        context = ""

        for index, paper in enumerate(papers, start=1):

            metadata = paper.get("metadata", {})

            paper_name = (
                    metadata.get("paper_name")
                    or metadata.get("title")
                    or f"Paper {index}"
            )

            sections = paper.get("sections", {})

            context += (
                f"\n\n"
                f"==================================================\n"
                f"PAPER {index}: {paper_name}\n"
                f"==================================================\n"
            )

            for heading, text in sections.items():

                heading_lower = heading.lower()

                if any(s in heading_lower for s in IMPORTANT_SECTIONS):
                    context += (
                        f"\n## {heading}\n"
                        f"{text[:SECTION_LIMIT]}\n"
                    )

        print("=" * 80)
        print("Context Length:", len(context))
        print("=" * 80)

        return context

    def compare_papers(self, papers):

        context = self.build_papers_context(papers)

        prompt = f"""
    You are ResearchPilot.

    Compare ONLY the papers provided below.

    Use ONLY the supplied context.

    Do NOT use outside knowledge.

    If information is missing, explicitly write:
    "Not discussed in this paper."

    ==========================
    PAPERS
    ==========================

    {context}

    ==========================

    Generate:

    # Quick Comparison Table

    One markdown table.

    Columns = paper names.

    Rows:

    - Research Problem
    - Core Idea
    - Methodology
    - Architecture
    - Datasets
    - Results
    - Strengths
    - Limitations

    # Executive Summary

    # Key Differences

    # Strengths & Weaknesses

    # Research Contributions

    # Final Verdict

    For every claim add

    (Source: Paper → Section)

    Do NOT generate Research Gaps.
    Do NOT generate Literature Review.
    """

        completion = self.client.chat.completions.create(
            model=QUALITY_MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
            temperature=0.2,
        )

        return completion.choices[0].message.content

    def research_gaps(self, papers):

        context = self.build_papers_context(papers)

        prompt = f"""
        You are ResearchPilot.

        You are performing a CRITICAL CROSS-PAPER RESEARCH GAP ANALYSIS.

        Analyze ONLY the selected uploaded papers below.

        =================================================
        SELECTED PAPERS
        =================================================

        {context}

        =================================================

        RULES

        - Use ONLY the selected uploaded papers.
        - Never use outside knowledge.
        - Never mention papers that appear only in references/citations.
        - Never invent methods, datasets, limitations or future work.
        - If something is not discussed, explicitly state:
          "Not discussed in the selected papers."
        - Never repeat the same fact in multiple sections.
        - Every section must contribute NEW information.
        - Use the uploaded paper names exactly as provided.
        - Every factual statement must end with:
          (Source: <Paper Name> → <Section>)

        =================================================

        # 1. Paper-wise Critical Review

        For EACH selected paper provide ONLY:

        Paper Name

        Objective

        Core Method

        Key Contributions

        Strengths

        Author-identified Limitations

        Author-proposed Future Work

        Discuss ONLY that paper.
        Do NOT compare papers here.

        -------------------------------------------------

        # 2. Cross-Paper Analysis

        Compare the selected papers.

        Discuss ONLY:

        • Common research problem

        • Major methodological differences

        • Similarities

        • Differences

        • Strength comparison

        • Weakness comparison

        Do NOT summarize papers again.
        Do NOT repeat facts from Section 1.

        -------------------------------------------------

        # 3. Research Gaps

        Infer research gaps ONLY AFTER comparing ALL papers.

        A research gap must represent something that remains unsolved across the selected papers.

        For EACH gap provide:

        Gap

        Why it remains unsolved

        Which papers partially address it

        Why existing approaches are insufficient

        Potential research direction

        Support every gap using the selected papers.

        If no common gap exists, write:

        "No common research gap could be inferred."

        -------------------------------------------------

        # 4. Missing Evaluations

        Identify evaluation aspects missing from the selected papers such as:

        • datasets

        • benchmarks

        • scalability

        • efficiency

        • latency

        • robustness

        • real-world deployment

        • ablation studies

        Only include evaluation gaps supported by the selected papers.

        Do NOT repeat methodological limitations.

        -------------------------------------------------

        # 5. Contradictions

        Identify genuine disagreements between papers.

        Examples:

        • conflicting assumptions

        • conflicting conclusions

        • different architectural choices

        • different evaluation methodology

        If none exist, explicitly state:

        "No significant contradictions were identified."

        -------------------------------------------------

        # 6. Future Research Directions

        Merge future work proposed by different papers.

        Remove duplicate ideas.

        Highlight the most promising future direction and explain WHY.

        -------------------------------------------------

        # 7. Thesis Opportunities

        Generate THREE concrete thesis ideas.

        Each idea MUST combine concepts from at least TWO selected papers.

        For each idea provide:

        Title

        Motivation

        Combined Papers

        Expected Contribution

        Implementation Challenge

        Avoid generic AI project ideas.

        -------------------------------------------------

        # Final Takeaway

        Write ONE concise analytical paragraph describing:

        • what these papers collectively achieve,

        • what still remains unsolved,

        • where future research should focus.

        Do NOT repeat previous sections.
        Do NOT summarize every paper again.
        """
        completion = self.client.chat.completions.create(
            model=QUALITY_MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
            temperature=0,
        )

        return completion.choices[0].message.content