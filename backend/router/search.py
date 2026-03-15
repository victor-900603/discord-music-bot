from fastapi import APIRouter, Request, Depends

from utils.dependencies import check_session
from utils.download import search_youtube

router = APIRouter()


@router.get("/")
async def search(request: Request, keyword: str, session=Depends(check_session)):
    """搜尋 YouTube 影片"""
    results = await search_youtube(keyword)
    return results
