from .client import GroqClient
from .prompts import SYSTEM_PROMPT


class LLMService:

    def __init__(self):

        self.client = GroqClient().client

    def answer(self, question, search_results):

        context = "\n\n".join(
            result.content
            for result in search_results
        )

        prompt = f"""
Context:

{context}

Question:

{question}
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