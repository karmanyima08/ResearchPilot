def detect_chat_intent(question: str):

    q = question.lower()

    if any(x in q for x in [
        "compare",
        "difference",
        "vs",
        "versus",
        "better than"
    ]):
        return "compare"

    if any(x in q for x in [
        "literature review",
        "related work",
        "survey",
        "state of the art",
        "summarize these papers"
    ]):
        return "literature"

    if any(x in q for x in [
        "research gap",
        "research gaps",
        "open problem",
        "open problems"
    ]):
        return "gaps"

    return "chat"