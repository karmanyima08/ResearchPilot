import json
from pathlib import Path


class PaperLookupService:

    STORAGE_ROOT = Path("storage/papers")

    def load_paper(self, paper_id: str):

        parsed_path = (
            self.STORAGE_ROOT
            / paper_id
            / "parsed.json"
        )

        if not parsed_path.exists():
            return None

        with parsed_path.open(
            "r",
            encoding="utf-8"
        ) as file:
            return json.load(file)

    def get_section(
        self,
        paper_id: str,
        section: str
    ):

        paper = self.load_paper(paper_id)

        if paper is None:
            return None

        sections = paper.get("sections", {})

        section = section.lower()

        for heading, content in sections.items():

            if section in heading.lower():
                return {
                    "heading": heading,
                    "content": content
                }

        return None

    def get_sections(
        self,
        paper_id: str,
        section_names: list[str]
    ):

        paper = self.load_paper(paper_id)

        if paper is None:
            return []

        sections = paper.get("sections", {})

        matched = []

        for heading, content in sections.items():

            heading_lower = heading.lower()

            for section_name in section_names:

                section_name = section_name.lower()

                if (
                    heading_lower == section_name
                    or section_name in heading_lower
                ):

                    matched.append(
                        {
                            "heading": heading,
                            "content": content
                        }
                    )

                    break

        return matched

    def get_all_sections(
        self,
        paper_id: str
    ):

        paper = self.load_paper(paper_id)

        if paper is None:
            return {}

        return paper.get("sections", {})