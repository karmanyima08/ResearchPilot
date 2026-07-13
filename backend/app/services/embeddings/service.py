from .model import EmbeddingModel


class EmbeddingService:

    def __init__(self):
        self.model = EmbeddingModel()

    def embed_chunks(self, chunks):

        texts = [
            chunk.content
            for chunk in chunks
        ]

        embeddings = self.model.encode(texts)

        return embeddings