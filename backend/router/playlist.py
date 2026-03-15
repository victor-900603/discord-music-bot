from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi import status

import asyncio
import logging

from utils.dependencies import check_session, get_playlist
from utils.playing_list import Playlist
from utils.download import download_audio
from utils.db import get_songs

logger = logging.getLogger("uvicorn")

router = APIRouter()


@router.post("/")
async def add(request: Request, id: str, mode: str = 'song', session=Depends(check_session), playlist: Playlist = Depends(get_playlist)):
    """加入歌曲或整個收藏清單到播放列表"""
    async def download_and_add_song(song_id: str):
        url = f'https://www.youtube.com/watch?v={song_id}'
        song_info = await download_audio(url)
        playlist.add_song(song_info)

    if mode == "song":
        await download_and_add_song(id)
    elif mode == "favorite":
        name, songs = await get_songs(session['user_id'], id)
        await asyncio.gather(*[download_and_add_song(song['id']) for song in songs])
    else:
        raise HTTPException(status_code=400, detail="Invalid mode. Use 'song' or 'favorite'.")

    return {"message": "Added to playlist"}


@router.get("/")
async def get_playlist_songs(playlist: Playlist = Depends(get_playlist)):
    """取得當前播放列表"""
    songs, current_index = playlist.view_playlist()
    return {
        "songs": [
            {
                "title": s["title"],
                "webpage_url": s["webpage_url"],
                "thumbnail": s["thumbnail"],
                "channel": s["channel"],
            } for s in songs
        ],
        "current_index": current_index,
        "loop": playlist.loop_queue,
        "shuffle": playlist.shuffle,
    }


@router.delete("/")
async def remove_song(index: int, playlist: Playlist = Depends(get_playlist)):
    """從播放列表移除指定歌曲"""
    song = playlist.remove_song(index)
    if not song:
        raise HTTPException(status_code=404, detail="Song not found")

    return {
        "message": "Song removed from playlist",
        "title": song["title"],
    }


@router.put("/move/")
async def move_song(from_index: int, to_index: int, playlist: Playlist = Depends(get_playlist)):
    """移動播放列表中的歌曲位置"""
    success = playlist.move_song(from_index, to_index)
    if not success:
        raise HTTPException(status_code=400, detail="Invalid index")
    return {"message": "Song moved successfully"}

