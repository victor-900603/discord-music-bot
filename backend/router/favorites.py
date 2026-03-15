from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import JSONResponse
from fastapi import status

from utils.dependencies import check_session
from utils.db import (
    get_favorites, add_favorite, delete_favorite,
    get_songs, insert_song, remove_song
)
from utils.models import Song

router = APIRouter()


# ==================== Favorites ====================

@router.get("/")
async def get_user_favorites(request: Request, session=Depends(check_session)):
    """取得使用者所有收藏清單"""
    favorites = await get_favorites(session['user_id'])
    return {
        "message": "Favorites get successfully.",
        "result": favorites,
    }


@router.post("/")
async def add_user_favorite(request: Request, name: str, session=Depends(check_session)):
    """新增收藏清單"""
    inserted_id = await add_favorite(session['user_id'], name)
    return {
        "message": "Favorite added successfully.",
        "result": inserted_id,
    }


@router.delete("/{id}/")
async def delete_user_favorite(request: Request, id: str, session=Depends(check_session)):
    """刪除收藏清單"""
    deleted_count = await delete_favorite(session['user_id'], id)
    if deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Favorite not found."
        )
    return {
        "message": "Favorite deleted successfully.",
        "result": deleted_count,
    }


# ==================== Songs in Favorites ====================

@router.post("/{favorite_id}/song/")
async def add_song_to_favorite(request: Request, favorite_id: str, song: Song, session=Depends(check_session)):
    """加入歌曲到指定收藏清單"""
    result = await insert_song(session['user_id'], favorite_id, song)
    matched_count, modified_count = result.values()
    if matched_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Favorite not found."
        )
    elif modified_count == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Song already exists in the favorite."
        )
    return {
        "message": "Song added successfully.",
        "status": "success",
    }


@router.get("/{favorite_id}/songs/")
async def get_song_from_favorite(request: Request, favorite_id: str, session=Depends(check_session)):
    """取得收藏清單中的所有歌曲"""
    name, songs = await get_songs(session['user_id'], favorite_id)
    return {
        "message": "Songs get successfully.",
        "result": {
            "name": name,
            "songs": songs,
        },
    }


@router.delete("/{favorite_id}/song/{song_id}/")
async def remove_song_from_favorite(request: Request, favorite_id: str, song_id: str, session=Depends(check_session)):
    """從收藏清單中移除歌曲"""
    result = await remove_song(session['user_id'], favorite_id, song_id)
    matched_count, modified_count = result.values()
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
    return {
        "message": "Song removed successfully.",
        "status": "success",
    }