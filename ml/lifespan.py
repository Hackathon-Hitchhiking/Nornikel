import torch
from loguru import logger
from colpali_engine.models import ColQwen2, ColQwen2Processor

from ml.config import ModelKwargs
from ml.constants import COLPALI_MODEL_NAME, LLM_PATH
from ml.llm import LLama3Quantized

device = "cuda" if torch.cuda.is_available() else "cpu"

logger.debug("loading embedder")

embedding_model = ColQwen2.from_pretrained(
    COLPALI_MODEL_NAME,
    torch_dtype=torch.bfloat16,
    device_map=device,  # or "mps" if on Apple Silicon
).eval()

embedding_processor = ColQwen2Processor.from_pretrained(COLPALI_MODEL_NAME)

llm = LLama3Quantized()


kwargs = ModelKwargs(
    temperature=0.7,
    top_k=30,
    top_p=0.9,
    max_tokens=8192,
    repeat_penalty=1.1,
)

llm.load_model(kwargs, LLM_PATH)
