from fastapi import APIRouter, Request, Depends, HTTPException, status
from fastapi.responses import JSONResponse

from discord.ext.commands import Bot
from utils.auth_token import decode_token
from utils.dependencies import check_session

router = APIRouter()

@router.get("/set")
async def auth(request: Request, token: str) -> JSONResponse:
    user_info = decode_token(token)
    if user_info is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
    request.session.update(user_info)
    
    bot: Bot = request.app.state.bot
    guild = bot.get_guild(request.session["guild_id"])
    user = guild.get_member(request.session["user_id"])

    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "message": "Session is set",
            'user': user.name,
            'guild': guild.name,
        }
    )

@router.get("/")
async def read_session(request: Request, session_data=Depends(check_session)):
    bot: Bot = request.app.state.bot
    guild = bot.get_guild(request.session["guild_id"])
    user = guild.get_member(request.session["user_id"])
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            'user': user.name,
            'guild': guild.name,
        }
    )

@router.delete("/")
async def delete_session(request: Request, session_data=Depends(check_session)):
    request.session.clear()
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={"message": "Session is deleted"}
    )