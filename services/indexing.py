import uuid

from fastapi import Depends
from io import BytesIO

from repositories.integration import BaseIntegrator
from services.minio import MinioService


class IndexingService:
    def __init__(self, minio: MinioService = Depends()):
        self._minio = minio

    def integrate_external(self, page_id: str, integrator: BaseIntegrator):
        content = integrator.fetch_data(page_id)

    def indexing_pdf(self, title: str, pdf: bytes):
        id = uuid.uuid4()
        minio_path = self._minio.save_pdf(id, title, BytesIO(pdf))

    def indexing_docx(self, title: str, docx: bytes):
        id = uuid.uuid4()
        minio_path = self._minio.save_docx(id, title, BytesIO(docx))
