from pathlib import Path
import json


class PaperService:

    STORAGE = Path("storage/papers")

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

        return papers