from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi import status

import asyncio

from utils.dependencies import check_session, get_user_voice_channel, get_playlist
from utils.playing_list import GuildPlaylistsManager, Playlist
from utils.download import download_audio
from utils.db import get_songs

router = APIRouter()

@router.post("/")
async def add(request: Request, id: str, mode: str= 'song', session= Depends(check_session), playlist= Depends(get_playlist)):
    async def download_and_add_song(id: str):
        url = f'https://www.youtube.com/watch?v={id}'
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
        print(f"Error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            # detail=str(e)
        )
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "message": "Added to playlist",
        }
    )
    
@router.get("/get")
async def get(request: Request, playlist= Depends(get_playlist)):
    try:
        songs, current_index = playlist.view_playlist()
        songs = list(map(lambda song: {
            "title": song["title"],
            "webpage_url": song["webpage_url"],
            "thumbnail": song["thumbnail"],
            "channel": song["channel"],
        }, songs))
    except HTTPException:
        raise
            
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    return JSONResponse(   
        status_code=status.HTTP_200_OK,
        content={
            "songs": songs,
            "current_index": current_index,
            "loop": playlist.loop_queue,
        }
    )
    
@router.get("/remove")
async def remove(request: Request, index: int, playlist= Depends(get_playlist)):
    try:
        song = playlist.remove_song(index)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    return JSONResponse(   
        status_code=status.HTTP_200_OK,
        content={
            "message": "Song removed from playlist",
            "title": song["title"],
        }
    )
