from fastapi import APIRouter, Request, Depends, HTTPException, Cookie
from fastapi.responses import JSONResponse
from fastapi import status

from fastapi.websockets import WebSocketDisconnect, WebSocket, WebSocketState
from fastapi.exceptions import HTTPException, WebSocketException

import logging
from discord import VoiceChannel
from discord.ext.commands import Bot
import asyncio
from utils.playback import play_song, pause_song, resume_song, skip_song
from utils.dependencies import check_session, get_user_voice_channel, get_playlist
from utils.playing_list import GuildPlaylistsManager, Playlist

logger = logging.getLogger("uvicorn")

router = APIRouter()

@router.websocket("/")
async def playbakc_ws(websocket: WebSocket, playlist: Playlist=Depends(get_playlist)):
    await websocket.accept()
    try:
        prev_data = None
        while True:            
            songs, current_index = playlist.view_playlist()
            songs = list(map(lambda song: {
                "title": song["title"],
                "webpage_url": song["webpage_url"],
                "thumbnail": song["thumbnail"],
                "channel": song["channel"],
            }, songs))
            data = {
                "is_playing": playlist.voice_client.is_playing(),
                "songs": songs,
                "current_index": current_index,
                "loop": playlist.loop_queue,
            }
            if data != prev_data:
                await websocket.send_json(data)
                prev_data = data
            await asyncio.sleep(1)
    except WebSocketDisconnect  as e:
        pass
    except Exception as e:
        logger.error(f"WebSocket error: {str(e)}")
        await websocket.close()
    finally:
        pass
    

@router.get("/play")
async def play(request: Request, playlist: Playlist=Depends(get_playlist)):
    try:
        bot: Bot = request.app.state.bot
        if not playlist.voice_client.is_playing() and not playlist.voice_client.is_paused():
            if playlist.is_end(): playlist.reset_index()
            play_song(bot, playlist.voice_client, playlist)
        elif playlist.voice_client.is_paused():
            resume_song(playlist.voice_client)
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "message": "Playing song",
                "title": playlist.songs[playlist.current_index]["title"],
            }
        )
    except Exception as e:
        logger.error(f"Error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

@router.get("/pause")
async def pause(request: Request, playlist: Playlist=Depends(get_playlist)):
    try:
        pause_song(playlist.voice_client)
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "message": "Paused song",
            }
        )
    except Exception as e:
        logger.error(f"Error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
        
@router.get("/skipto")
async def skipto(request: Request, index:int, playlist: Playlist=Depends(get_playlist)):
    try:
        song = playlist.skip_to(index)
        if song is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid index"
            )
        
        bot: Bot = request.app.state.bot
          
        if not playlist.voice_client.is_playing() and not playlist.voice_client.is_paused():
            play_song(bot, playlist.voice_client, playlist)
        elif playlist.voice_client.is_paused():
            resume_song(playlist.voice_client)
            skip_song(playlist.voice_client)
        elif playlist.voice_client.is_playing():
            skip_song(playlist.voice_client)
            
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "message": "Skipped song",
                "title": song["title"],
            }
        )
    except Exception as e:
        logger.error(f"Error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
        
@router.get("/loop")
async def loop(request: Request, playlist: Playlist=Depends(get_playlist)):
    try:
        playlist.loop_queue = not playlist.loop_queue
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "message": "Looping song",
                "loop": playlist.loop_queue,
            }
        )
    except Exception as e:
        logger.error(f"Error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
        