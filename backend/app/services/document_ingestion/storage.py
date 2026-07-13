from pathlib import Path
from uuid import uuid4
import shutil
from fastapi import UploadFile


class StorageService:
    def __init__(self):
        self.storage_root = Path("storage/papers")

    def save_pdf(self, file: UploadFile):
        # Generate unique paper ID
        paper_id = str(uuid4())

        # Create paper directory
        paper_folder = self.storage_root / paper_id
        paper_folder.mkdir(parents=True, exist_ok=True)

        # Save original PDF
        pdf_path = paper_folder / "original.pdf"

        with pdf_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        return {
            "paper_id": paper_id,
            "paper_folder": paper_folder,
            "pdf_path": pdf_path
        }

    def save_markdown(self, paper_folder: Path, markdown: str):
        markdown_path = paper_folder / "parsed.md"

        print("Writing markdown length:", len(markdown))

        with markdown_path.open("w", encoding="utf-8") as file:
            file.write(markdown)

        print("Saved file size:", markdown_path.stat().st_size)

        return markdown_path
        """
        Save the parsed markdown representation of the paper.
        """

        markdown_path = paper_folder / "parsed.md"

        with markdown_path.open("w", encoding="utf-8") as file:
            file.write(markdown)

        return markdown_path