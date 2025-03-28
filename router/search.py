from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi import status

from utils.dependencies import check_session
from utils.download import search_yotube


router = APIRouter()


@router.get("/")
async def search(request: Request, keyword: str, dependencies= Depends(check_session)):
    try:
        results = await search_yotube(keyword)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
        
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=results
    )
