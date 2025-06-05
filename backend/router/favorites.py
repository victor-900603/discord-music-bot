from fastapi import APIRouter, Request, Depends, HTTPException, Cookie
from fastapi.responses import JSONResponse
from fastapi import status

from fastapi.exceptions import HTTPException


from utils.dependencies import check_session, get_playlist
from utils.db import *
from utils.models import Song

router = APIRouter()

# Favorites
@router.get("/")
async def get_user_favorites( request: Request, session= Depends(check_session)):
    try:
        favorites = await get_favorites(session['user_id'])
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "result": favorites,
            }
        )
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
        
@router.delete("/{id}")
async def delete_user_favorite( request: Request, id: str, session= Depends(check_session)):
    try:
        deleted_count = await delete_favorite(session['user_id'], id)
        if deleted_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Favorite not found."
            )
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "result": deleted_count,
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
        
@router.post("/")
async def delete_user_favorite( request: Request, name: str, session= Depends(check_session)):
    try:
        inserted_id = await add_favorite(session['user_id'], name)
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "result": inserted_id,
            }
        )
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


# Songs
@router.post("/{favorite_id}/song")
async def add_song_to_favorite( request: Request, favorite_id: str, song: Song, session= Depends(check_session)):
    try:
        matched_count, modified_count = (await insert_song(session['user_id'], favorite_id, song)).values()
        if matched_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Favorite not found."
            )
        elif modified_count == 0: # song already exists
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Song already exists in the favorite."
            )
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "status": 'success',
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
        
@router.get("/{favorite_id}/song")
async def get_song_from_favorite( request: Request, favorite_id: str, session= Depends(check_session)):
    try:
        songs = await get_songs(session['user_id'], favorite_id)
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "result": songs,
            }
        )
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )
        
@router.delete("/{favorite_id}/song/{song_id}")
async def remove_song_from_favorite( request: Request, favorite_id: str, song_id: str, session= Depends(check_session)):
    try:
        matched_count, modified_count = (await remove_song(session['user_id'], favorite_id, song_id)).values()
            
        if matched_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Favorite not found."
            )
        elif modified_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Song isn't in the favorite."
            )
        return JSONResponse(
            status_code=status.HTTP_200_OK,
            content={
                "status": 'success',
            }
        )
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )