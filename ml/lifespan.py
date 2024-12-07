import torch
from loguru import logger
from colpali_engine.models import ColQwen2, ColQwen2Processor

from ml.constants import COLPALI_MODEL_NAME

device = "cuda" if torch.cuda.is_available() else "cpu"

logger.debug("loading embedder")

embedding_model = ColQwen2.from_pretrained(
    COLPALI_MODEL_NAME,
    torch_dtype=torch.bfloat16,
    device_map=device,  # or "mps" if on Apple Silicon
).eval()

embedding_processor = ColQwen2Processor.from_pretrained(COLPALI_MODEL_NAME)
