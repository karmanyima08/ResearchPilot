from .client import GroqClient
from .prompts import SYSTEM_PROMPT
class LLMService:

    def __init__(self):
        self.client = GroqClient().client

    def answer(self,question, search_results, history=[]):
        context = "\n\n".join(
            result.content[:800]
            for result in search_results
        )

        prompt = f"""
        Context

        {context}

        ------------------------

        Question

        {question}

        ------------------------

        Instructions

        Answer in this format:

        ## Answer

        Provide a clear explanation.

        ## Key Points

        - Bullet point 1
        - Bullet point 2
        - Bullet point 3

        ## Simple Explanation

        Explain like you're teaching a university student who is new to the topic.

        ## Takeaway

        One sentence summarizing the idea.
        """

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

            model="llama-3.1-8b-instant",

            messages=messages,

            temperature=0.2

        )
        return completion.choices[0].message.content

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

            model="llama-3.1-8b-instant",

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

    def literature_review(self, search_results):

        context = "\n\n".join(
            result.content
            for result in search_results
        )

        prompt = f"""
        You are ResearchPilot, an expert AI research assistant.

        Use ONLY the provided context.

        Context:
        {context}

        ------------------------


        Respond in this format:

        ## 📖 Answer
        Give a clear and accurate answer.

        ## 🔑 Key Points
        - Point 1
        - Point 2
        - Point 3

        ## 💡 Simple Explanation
        Explain as if teaching a beginner.

        ## ✅ Takeaway
        Summarize the idea in one sentence.

        If the answer is not supported by the context, say:
        "I couldn't find enough evidence in the selected papers."
        """

        completion = self.client.chat.completions.create(

            model="llama-3.1-8b-instant",

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

    def compare_papers(self, search_results):
        context = "\n\n".join(
            result.content
            for result in search_results
        )

        prompt = f"""
        You are an expert research analyst.

        Compare ONLY the selected research papers using the context below.

        Context:
        {context}

        Rules:
        - Use ONLY the provided context.
        - If information is missing, write "Not specified."
        - Use Markdown.
        - Keep the comparison factual.

        Your response MUST follow exactly this format:

        # 📖 Overview

        Briefly describe what all selected papers are about.

        # 📊 Comparison Table

        | Aspect | Paper 1 | Paper 2 |
        |--------|---------|---------|
        | Research Goal | | |
        | Methodology | | |
        | Main Contribution | | |
        | Strengths | | |
        | Weaknesses | | |
        | Best Use Case | | |

        (If more than two papers are selected, add more columns.)

        # 🤝 Similarities

        - ...

        # ⚖️ Differences

        - ...

        # 🚧 Research Gaps

        - ...

        # 🚀 Future Research Directions

        - ...

        # ✅ Conclusion

        Recommend when each paper should be preferred.
        """

        completion = self.client.chat.completions.create(

            model="llama-3.1-8b-instant",

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

    def rewrite_query(
            self,
            question: str,
            history: list = []
    ):

        conversation = ""

        for msg in history[-6:]:
            role = msg.role if hasattr(msg, "role") else msg["role"]
            content = msg.content if hasattr(msg, "content") else msg["content"]

            conversation += f"{role}: {content}\n"

        question_lower = question.lower()

        pronouns = [
            "it",  "its",  "they",  "them", "their","this", "that",  "these", "those",  "he",  "she"
        ]

        # If the question already looks complete, don't rewrite it.
        if not any(f" {p} " in f" {question_lower} " for p in pronouns):
            return question

        prompt = f"""
    Conversation:

    {conversation}

    Current Question:

    {question}

    Rewrite the current question so it is completely self-contained.

    Rules:
    - Replace words like "it", "they", "that paper", "this method".
    - Keep the same meaning.
    - Return ONLY the rewritten question.
    - Do not answer the question.
    """

        completion = self.client.chat.completions.create(
            model="llama-3.1-8b-instant",
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

        return completion.choices[0].message.content.strip()

    def research_gaps(self, search_results):

        context = "\n\n".join(
            result.content[:800]
            for result in search_results
        )

        prompt = f"""
    You are an expert research analyst.

    Use ONLY the context below.

    Context:
    {context}

    Write a report in Markdown.

    # 🔍 Research Gaps

    Identify important limitations in the selected papers.

    # 💡 Potential Research Ideas

    Suggest 4 novel research ideas.

    # 🚀 Future Work

    Suggest future research directions.

    Do not invent information.
    If evidence is missing, say so.
    """

        completion = self.client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2
        )

        return completion.choices[0].message.content