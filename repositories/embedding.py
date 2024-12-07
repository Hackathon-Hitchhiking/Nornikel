import io

import torch
from PIL import Image

from ml.lifespan import device, embedding_model, embedding_processor


class EmbeddingRepository:
    def __init__(self):
        self.device = device

    def extract_text_embedding(self, text: str) -> torch.Tensor:
        with torch.inference_mode():
            processed_text = embedding_processor.process_queries(text).to(self.device)
            text_embedding = embedding_model(processed_text)

        return text_embedding

    def extract_image_embeddings(self, image_bytes: bytes) -> torch.Tensor:
        with torch.inference_mode():
            image = Image.open(io.BytesIO(image_bytes))
            processed_image = embedding_processor.process_queries(image).to(self.device)
            image_embedding = embedding_model(processed_image)

        return image_embedding
