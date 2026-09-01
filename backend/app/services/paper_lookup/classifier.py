SECTION_MAP = {
    "abstract": ["abstract"],

    "introduction": ["introduction", "background"],
    "background": ["introduction", "background"],

    "related work": ["related work", "literature review"],
    "literature review": ["related work", "literature review"],

    "method": [
    "methodology",
],

"methods": [
    "methodology",
],
    "methodology": [
    "methodology",
],

    "experiment": ["experiments"],

    "results": ["results"],

    "discussion": ["discussion"],


    "conclusion": [
        "conclusion",
    ],

    "limitations": [
        "limitations",
        "discussion",
        "conclusion",
    ],
    "limitation": [
        "limitations",
        "discussion",
        "conclusion",
    ],

    "future work": [
        "future_work",
        "conclusion",
    ],

    "authors": [
        "front_matter",
    ],

    "author": [
        "front_matter",
    ]
}


def detect_requested_section(question: str):

    question = question.lower()

    for keyword, sections in SECTION_MAP.items():

        if keyword in question:
            return sections

    return None