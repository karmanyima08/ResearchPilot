from pathlib import Path
import json
import shutil
from app.services.vector_store.chroma_client import ChromaClient
class PaperService:

    STORAGE = Path("storage/papers")

    db = ChromaClient()
    def list_papers(self):

        papers = []

        if not self.STORAGE.exists():
            return papers

        for folder in self.STORAGE.iterdir():

            if folder.is_dir():

                metadata_file = folder / "metadata.json"

                if metadata_file.exists():

                    with open(metadata_file, "r", encoding="utf-8") as f:
                        papers.append(json.load(f))

        papers.sort(
                    key=lambda paper: paper.get("uploaded_at", ""),
                    reverse=True
                )

        return papers

    def exists(self, paper_name: str) -> bool:

        papers = self.list_papers()

        return any(
            paper["paper_name"].lower() == paper_name.lower()
            for paper in papers
        )

    def delete_paper(self, paper_id: str):

        folder = self.STORAGE / paper_id

        if not folder.exists():
            return {
                "success": False,
                "message": "Paper not found."
            }

        # Delete vectors from Chroma
        self.db.collection.delete(
            where={
                "paper_id": paper_id
            }
        )

        # Delete paper folder
        shutil.rmtree(folder)

        return {
            "success": True,
            "message": "Paper deleted successfully."
        }