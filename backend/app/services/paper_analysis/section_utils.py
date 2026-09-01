from typing import Dict

METHOD_KEYS = [
    "method",
    "methods",
    "methodology",
    "approach",
    "framework",
    "training",
    "implementation",
]

RESULT_KEYS = [
    "result",
    "results",
    "evaluation",
    "experiment",
    "experiments",
    "benchmark",
]

DISCUSSION_KEYS = [
    "discussion",
    "analysis",
    "limitations",
    "future work",
]

INTRODUCTION_KEYS = [
    "introduction",
    "background",
]

RELATED_WORK_KEYS = [
    "related work",
    "literature review",
]


def find_sections(
    sections: Dict[str, str],
    keywords: list[str],
) -> Dict[str, str]:
    """
    Return all sections whose heading contains one of the given keywords.
    """
    matched = {}

    for heading, content in sections.items():
        heading_lower = heading.lower()

        for keyword in keywords:
            if keyword in heading_lower:
                matched[heading] = content
                break

    return matched