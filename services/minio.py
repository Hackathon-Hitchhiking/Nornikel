import uuid
from io import BytesIO

from fastapi import Depends

from repositories.minio import MinioRepository
from schemas.minio import MinioContentType


class MinioService:
    def __init__(self, repo: MinioRepository = Depends()):
        self._repo = repo

    def save_pdf(self, id: uuid.UUID, title: str, file: BytesIO) -> str:
        return self._repo.create_object_from_byte(
            f"pdf/{id.__str__()}/{title}.pdf", file, MinioContentType.PDF
        )

    def save_docx(self, id: uuid.UUID, title: str, file: BytesIO) -> str:
        return self._repo.create_object_from_byte(
            f"docx/{id.__str__()}/{title}.docx", file, MinioContentType.DOCX
        )
