from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from fastapi import status


route = APIRouter()

@route.get("/")
async def play(request: Request, guild_id: str, playlist_name: str):
    """
    Play a playlist in the guild.
    """