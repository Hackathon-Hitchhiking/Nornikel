from fastapi import APIRouter, UploadFile, File, Depends

from schemas.search import SearchByTextRequest
from services.search import SearchService

router = APIRouter(prefix="/api/v1/search", tags=["search"])


@router.post("/image", summary="indexing the pdf file")
def search_by_image(
    search_service: SearchService = Depends(), image: UploadFile = File(...)
):
    return search_service.search_by_image(image.file.read())


@router.post("/text", summary="indexing the docx file")
def search_by_text(
    opts: SearchByTextRequest,
    search_service: SearchService = Depends(),
):
    return search_service.search_by_text(opts.text)
