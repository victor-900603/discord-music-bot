from fastapi import APIRouter, Request, Depends, HTTPException, Query
from fastapi import status

from fastapi.websockets import WebSocketDisconnect, WebSocket

import logging
from discord.ext.commands import Bot
import asyncio
from utils.playback import play_song, pause_song, resume_song, skip_song
from utils.dependencies import check_session, get_user_voice_channel, get_playlist
from utils.playing_list import Playlist

logger = logging.getLogger("uvicorn")

router = APIRouter()


def _serialize_songs(songs: list[dict]) -> list[dict]:
    """將歌曲列表轉換為前端所需格式"""
    return [
        {
            "title": song["title"],
            "webpage_url": song["webpage_url"],
            "thumbnail": song["thumbnail"],
            "channel": song["channel"],
        }
        for song in songs
    ]


@router.websocket("/")
async def playback_ws(websocket: WebSocket, playlist: Playlist = Depends(get_playlist)):
    """WebSocket 端點，即時推送播放狀態"""
    await websocket.accept()
    try:
        prev_data = None
        while True:
            songs, current_index = playlist.view_playlist()
            data = {
                "is_playing": playlist.voice_client.is_playing() if playlist.voice_client else False,
                "songs": _serialize_songs(songs),
                "current_index": current_index,
                "loop": playlist.loop_queue,
                "shuffle": playlist.shuffle,
                "volume": playlist.volume,
            }
            if data != prev_data:
                await websocket.send_json(data)
                prev_data = data.copy()
            await asyncio.sleep(1)
    except WebSocketDisconnect:
        pass
    except Exception as e:
        logger.error(f"WebSocket error: {str(e)}")
        try:
            await websocket.close()
        except Exception:
            pass


@router.get("/play/")
async def play(request: Request, playlist: Playlist = Depends(get_playlist)):
    """播放或恢復播放"""
    bot: Bot = request.app.state.bot
    if not playlist.voice_client.is_playing() and not playlist.voice_client.is_paused():
        if playlist.is_end():
            playlist.reset_index()
        play_song(bot, playlist.voice_client, playlist)
    elif playlist.voice_client.is_paused():
        resume_song(playlist.voice_client)
    
    current = playlist.current_info()
    return {
        "message": "Playing song",
        "title": current["title"] if current else "",
    }


@router.get("/pause/")
async def pause(request: Request, playlist: Playlist = Depends(get_playlist)):
    """暫停播放"""
    pause_song(playlist.voice_client)
    return {"message": "Paused song"}


@router.get("/skipto/")
async def skipto(request: Request, index: int, playlist: Playlist = Depends(get_playlist)):
    """跳至指定歌曲"""
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

    return {
        "message": "Skipped song",
        "title": song["title"],
    }


@router.get("/loop/")
async def loop(request: Request, playlist: Playlist = Depends(get_playlist)):
    """切換循環播放"""
    playlist.loop_queue = not playlist.loop_queue
    return {
        "message": f"Loop {'enabled' if playlist.loop_queue else 'disabled'}",
        "loop": playlist.loop_queue,
    }


@router.get("/shuffle/")
async def shuffle(request: Request, playlist: Playlist = Depends(get_playlist)):
    """切換隨機播放"""
    new_state = playlist.toggle_shuffle()
    return {
        "message": f"Shuffle {'enabled' if new_state else 'disabled'}",
        "shuffle": new_state,
    }


@router.get("/volume/")
async def volume(
    request: Request,
    value: float = Query(..., ge=0.0, le=1.0, description="音量值 (0.0 ~ 1.0)"),
    playlist: Playlist = Depends(get_playlist),
):
    """設定播放音量"""
    actual_volume = playlist.set_volume(value)
    return {
        "message": f"Volume set to {actual_volume:.0%}",
        "volume": actual_volume,
    }
