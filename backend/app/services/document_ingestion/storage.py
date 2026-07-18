from pathlib import Path
from uuid import uuid4
import shutil
import json

from fastapi import UploadFile


class StorageService:

    def __init__(self):
        self.storage_root = Path("storage/papers")

    def save_pdf(self, file: UploadFile):

        paper_id = str(uuid4())

        paper_folder = self.storage_root / paper_id
        paper_folder.mkdir(parents=True, exist_ok=True)

        pdf_path = paper_folder / "original.pdf"

        with pdf_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        from datetime import datetime

        # Save paper metadata
        metadata = {
            "paper_id": paper_id,
            "paper_name": file.filename,
            "uploaded_at": datetime.now().isoformat(),

        }
        with (paper_folder / "metadata.json").open(
            "w",
            encoding="utf-8"
        ) as f:
            json.dump(metadata, f, indent=4)

        return {
            "paper_id": paper_id,
            "paper_folder": paper_folder,
            "pdf_path": pdf_path
        }

    def save_markdown(self, paper_folder: Path, markdown: str):

        markdown_path = paper_folder / "parsed.md"

        with markdown_path.open("w", encoding="utf-8") as file:
            file.write(markdown)

        return markdown_path