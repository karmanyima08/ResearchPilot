from .chroma_client import ChromaClient


class VectorStoreService:

    def __init__(self):

        self.db = ChromaClient()

    def store(self, chunks, embeddings):

        ids = []
        documents = []
        metadatas = []

        for chunk in chunks:

            ids.append(str(chunk.chunk_id))

            documents.append(chunk.content)

            metadatas.append(chunk.metadata)

        self.db.collection.add(

            ids=ids,

            embeddings=embeddings.tolist(),

            documents=documents,

            metadatas=metadatas

        )