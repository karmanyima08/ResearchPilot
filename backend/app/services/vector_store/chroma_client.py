import chromadb


class ChromaClient:

    def __init__(self):

        self.client = chromadb.PersistentClient(
            path="storage/chroma"
        )

        self.collection = self.client.get_or_create_collection(
            name="research_papers"
        )