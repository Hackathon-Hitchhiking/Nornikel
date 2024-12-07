from qdrant_client.models import VectorParams, Distance
from qdrant_client.qdrant_client import QdrantClient

from configs.Environment import get_environment_variables

env = get_environment_variables()


client = QdrantClient(host=env.QDRANT_HOST, port=env.QDRANT_PORT)

if not client.collection_exists(env.QDRANT_COLLECTION):
    client.create_collection(
        collection_name=env.QDRANT_COLLECTION,
        vectors_config=VectorParams(size=100, distance=Distance.COSINE),
    )


def get_client() -> QdrantClient:
    yield client
