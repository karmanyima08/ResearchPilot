from pathlib import Path

from docling.document_converter import (
    DocumentConverter,
    PdfFormatOption,
)
from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import PdfPipelineOptions

from .parser import DocumentParser
from .models import ParsedDocument


class DoclingParser(DocumentParser):

    def __init__(self):
        pipeline_options = PdfPipelineOptions()

        # Optimize for born-digital research papers
        pipeline_options.do_ocr = False
        pipeline_options.force_backend_text = True
        pipeline_options.do_table_structure = True

        self.converter = DocumentConverter(
            format_options={
                InputFormat.PDF: PdfFormatOption(
                    pipeline_options=pipeline_options
                )
            }
        )

    def parse(self, pdf_path: Path) -> ParsedDocument:
        result = self.converter.convert(str(pdf_path))

        print("=" * 80)
        print("DOCUMENT METHODS")
        print("=" * 80)
        print(dir(result.document))
        print("=" * 80)

        markdown = result.document.export_to_markdown()

        return ParsedDocument(
            markdown=markdown
        )