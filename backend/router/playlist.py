from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi import status

import asyncio, logging

from utils.dependencies import check_session, get_user_voice_channel, get_playlist
from utils.playing_list import GuildPlaylistsManager, Playlist
from utils.download import download_audio
from utils.db import get_songs

logger = logging.getLogger("uvicorn")

router = APIRouter()

@router.post("/")
async def add(request: Request, id: str, mode: str='song', session=Depends(check_session), playlist=Depends(get_playlist)):
    async def download_and_add_song(song_id: str):
        url = f'https://www.youtube.com/watch?v={song_id}'
        song_info = await download_audio(url)
        playlist.add_song(song_info)

    try:
        if mode == "song":
            await download_and_add_song(id)
        elif mode == "favorite":
            name, songs = await get_songs(session['user_id'], id)
            asyncio.gather(*[download_and_add_song(song['id']) for song in songs])
        else:
            raise HTTPException(status_code=400, detail="Invalid mode")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error: {e}")
        raise HTTPException(status_code=500)
    
    return {"message": "Added to playlist"}


@router.get("/")
async def get_playlist_songs(playlist=Depends(get_playlist)):
    try:
        songs, current_index = playlist.view_playlist()
        songs = [
            {
                "title": s["title"],
                "webpage_url": s["webpage_url"],
                "thumbnail": s["thumbnail"],
                "channel": s["channel"],
            } for s in songs
        ]
    except Exception as e:
        logger.error(f"Error: {e}")
        raise HTTPException(status_code=500)

    return {
        "songs": songs,
        "current_index": current_index,
        "loop": playlist.loop_queue,
    }


@router.delete("/")
async def remove_song(index: int, playlist=Depends(get_playlist)):
    try:
        song = playlist.remove_song(index)
        if not song:
            raise HTTPException(status_code=404, detail="Song not found")
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500)

    return {
        "message": "Song removed from playlist",
        "title": song["title"],
    }

