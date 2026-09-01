from pathlib import Path

from docling.document_converter import (
    DocumentConverter,
    PdfFormatOption,
)
from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import PdfPipelineOptions
from docling.backend.pypdfium2_backend import PyPdfiumDocumentBackend

from .parser import DocumentParser
from .models import ParsedDocument
import re

MAJOR_SECTIONS = {
    "abstract": "abstract",

    "introduction": "introduction",
    "background": "introduction",

    "related work": "related_work",
    "literature review": "related_work",

    "method": "methodology",
    "methods": "methodology",
    "methodology": "methodology",
    "approach": "methodology",
    "framework": "methodology",

    "experiment": "experiments",
    "experiments": "experiments",
    "experimental setup": "experiments",
    "evaluation": "experiments",

    "result": "results",
    "results": "results",

    "discussion": "discussion",

    "limitation": "limitations",
    "limitations": "limitations",

    "future work": "future_work",

    "conclusion": "conclusion",

    "references": "references"
}

class DoclingParser(DocumentParser):
    import re

    def extract_sections(self, markdown: str):

        sections = {}

        current_section = "front_matter"

        sections[current_section] = ""

        for line in markdown.splitlines():

            line = line.rstrip()

            # Only markdown headings
            if re.match(r"^#{1,6}\s+", line):

                heading = re.sub(r"^#{1,6}\s+", "", line)

                heading = re.sub(r"^\d+(\.\d+)*\s*", "", heading)

                heading = heading.lower().strip()

                matched = None

                for key, canonical in MAJOR_SECTIONS.items():

                    if key in heading:
                        matched = canonical
                        break

                if matched:
                    current_section = matched

                    if current_section not in sections:
                        sections[current_section] = ""

                continue

            sections[current_section] += line + "\n"

        return sections






    def __init__(self):
        pipeline_options = PdfPipelineOptions()

        pipeline_options.do_ocr = False
        pipeline_options.force_backend_text = True
        pipeline_options.do_table_structure = True

        self.converter = DocumentConverter(
            format_options={
                InputFormat.PDF: PdfFormatOption(
                    pipeline_options=pipeline_options,
                    backend=PyPdfiumDocumentBackend,   # <-- the fix
                )
            }
        )

    def parse(self, pdf_path: Path) -> ParsedDocument:
        result = self.converter.convert(str(pdf_path))



        markdown = result.document.export_to_markdown()

        sections = self.extract_sections(markdown)

        for key in sections:
            print(key)

        print("\n========== SECTIONS ==========")

        for key in sections.keys():
            print("-", key)

        print("==============================")

        return ParsedDocument(
            markdown=markdown,
            sections=sections
        )





