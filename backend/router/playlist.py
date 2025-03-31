from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi import status

from utils.dependencies import check_session, get_user_voice_channel, get_playlist
from utils.playing_list import GuildPlaylistsManager, Playlist
from utils.download import download_audio

router = APIRouter()

@router.get("/add")
async def add(request: Request, id: str, playlist= Depends(get_playlist)):
    try:
        url = f'https://www.youtube.com/watch?v={id}'
        song_info = await download_audio(url)
        playlist.add_song(song_info)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            # detail=str(e)
        )
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "message": "Song added to playlist",
            "title": song_info["title"],
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
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    return JSONResponse(   
        status_code=status.HTTP_200_OK,
        content={
            "songs": songs,
            "current_index": current_index,
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
