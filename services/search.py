from fastapi import Depends

from repositories.embedding import EmbeddingRepository
from repositories.qdrant import QdrantRepository


class SearchService:
    def __init__(
        self,
        embedding_repo: EmbeddingRepository = Depends(),
        qdrant_repo: QdrantRepository = Depends(),
    ):
        self._embedding_repo = embedding_repo
        self._qdrant_repo = qdrant_repo

    def search_by_image(self, image: bytes):
        embedding = self._embedding_repo.extract_image_embeddings(image)

        documents = self._qdrant_repo.get_document(embedding.tolist(), 1)

        document = documents[0]

    def search_by_text(self, text: str):
        embedding = self._embedding_repo.extract_text_embedding(text)

        documents = self._qdrant_repo.get_document(embedding.tolist(), 1)

        document = documents[0]
