import uuid
from typing import Any

from fastapi import Depends
from io import BytesIO

from ml.indexing import PdfProcessor, DocxProcessor, PptxProcessor
from repositories.embedding import EmbeddingRepository
from repositories.integration import BaseIntegrator
from repositories.qdrant import QdrantRepository
from schemas.processor import CreateDocumentOpts
from services.minio import MinioService


class IndexingService:
    def __init__(
        self,
        minio: MinioService = Depends(),
        embedding: EmbeddingRepository = Depends(),
        qdrant_repo: QdrantRepository = Depends(),
    ):
        self._minio = minio
        self._embedding_repo = embedding
        self._qdrant_repo = qdrant_repo

    def integrate_external(self, page_id: str, integrator: BaseIntegrator):
        content = integrator.fetch_data(page_id)

        self._qdrant_repo.create_document(
            CreateDocumentOpts(
                vector=self._embedding_repo.extract_text_embeddings(content).tolist(),
                metadata={"source": integrator.source(), "page_id": page_id},
            )
        )

    def indexing_pdf(self, title: str, pdf: bytes):
        id = uuid.uuid4()
        minio_path = self._minio.save_pdf(id, title, BytesIO(pdf))

        processor = PdfProcessor()

        for chunk in processor.process(pdf):
            self._process_chunk(chunk, minio_path, id)

    def indexing_docx(self, title: str, docx: bytes):
        id = uuid.uuid4()
        minio_path = self._minio.save_docx(id, title, BytesIO(docx))

        processor = DocxProcessor()

        for chunk in processor.process(docx):
            self._process_chunk(chunk, minio_path, id)

    def indexing_pptx(self, title: str, pptx: bytes):
        id = uuid.uuid4()
        minio_path = self._minio.save_pptx(id, title, BytesIO(pptx))

        processor = PptxProcessor()

        for chunk in processor.process(pptx):
            self._process_chunk(chunk, minio_path, id)

    def _process_chunk(self, chunk: dict[str, Any], minio_path: str, id: uuid.UUID):
        text = chunk["chunk"]
        metadata = chunk["metadata"]

        images = metadata.pop("images", None)

        metadata["minio_path"] = minio_path
        metadata["text"] = text
        metadata["id"] = id

        for image in images:
            self._qdrant_repo.create_document(
                CreateDocumentOpts(
                    vector=self._embedding_repo.extract_image_embeddings(
                        image
                    ).tolist(),
                    metadata=metadata,
                )
            )

        self._qdrant_repo.create_document(
            CreateDocumentOpts(
                vector=self._embedding_repo.extract_text_embeddings(text).tolist(),
                metadata=metadata,
            )
        )
