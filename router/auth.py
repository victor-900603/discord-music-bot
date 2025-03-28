from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi import status
from utils.auth_token import decode_token
from utils.dependencies import check_session

router = APIRouter()

@router.get("/set")
async def auth(request: Request, token: str):
    user_info = decode_token(token)
    if user_info is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )

    request.session.update(user_info)
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"message": "Session is set"}
    )

@router.get("/get")
async def get(request: Request, dependencies= Depends(check_session)):
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content=request.session
    )

@router.get("/delete")
async def delete(request: Request, dependencies= Depends(check_session)):
    request.session.clear()
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"message": "Session is deleted"}
    )