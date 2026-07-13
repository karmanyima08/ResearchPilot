from app.services.llm.service import LLMService
from app.services.retrieval.service import RetrievalService

question = "What is Retrieval-Augmented Generation?"

retriever = RetrievalService()

results = retriever.search(question)

llm = LLMService()

answer = llm.answer(question, results)

print("=" * 80)
print(answer)
print("=" * 80)