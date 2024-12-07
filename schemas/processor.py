from typing import List, Any

from pydantic import BaseModel


class CreateDocumentOpts(BaseModel):
    vector: List[float]
    metadata: dict[str, Any]
