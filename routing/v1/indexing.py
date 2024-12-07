from fastapi import APIRouter, UploadFile, File, Depends

from repositories.integration import ConfluenceIntegration, NotionIntegration
from services.indexing import IndexingService

router = APIRouter(prefix="/api/v1/indexing", tags=["indexing"])


@router.post("/notion/{page_id}", summary="indexing the notion page")
def indexing_notion(
    page_id: str, api_token: str, indexing_service: IndexingService = Depends()
):
    indexing_service.integrate_external(page_id, NotionIntegration(api_token))


@router.post("/confluence/{page_id}", summary="indexing the confluence page")
def indexing_confluence(
    page_id: str,
    username: str,
    password: str,
    indexing_service: IndexingService = Depends(),
):
    indexing_service.integrate_external(
        page_id, ConfluenceIntegration(username, password)
    )


@router.post("/file/pdf", summary="indexing the pdf file")
def indexing_pdf(
    indexing_service: IndexingService = Depends(), pdf: UploadFile = File(...)
):
    indexing_service.indexing_pdf(pdf.filename, pdf.file.read())


@router.post("/file/docx", summary="indexing the docx file")
def indexing_docx(
    indexing_service: IndexingService = Depends(), docx: UploadFile = File(...)
):
    indexing_service.indexing_docx(docx.filename, docx.file.read())


@router.post("/file/pptx", summary="indexing the ptpx file")
def indexing_pptx(
    indexing_service: IndexingService = Depends(), pptx: UploadFile = File(...)
):
    indexing_service.indexing_pptx(pptx.filename, pptx.file.read())
