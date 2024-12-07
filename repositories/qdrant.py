import uuid
from typing import List

from qdrant_client.grpc import ScoredPoint
from qdrant_client.qdrant_client import QdrantClient

from configs.Qdrant import get_client, env
from schemas.processor import CreateDocumentOpts


class QdrantRepository:
    def __init__(self, client: QdrantClient = get_client()):
        self.client = client
        self.collection = env.QDRANT_COLLECTION

    def create_document(self, opts: List[CreateDocumentOpts]):
        self.client.upsert(
            collection_name=self.collection,
            points=[
                {
                    "id": uuid.uuid4().__str__(),
                    "vector": opt.vector,
                    "payload": opt.metadata,
                }
                for opt in opts
            ],
        )

    def get_document(self, query_vector: List[float], top_k: int) -> list[ScoredPoint]:
        hits = self.client.search(
            collection_name=self.collection, query_vector=query_vector, limit=top_k
        )
        return hits
