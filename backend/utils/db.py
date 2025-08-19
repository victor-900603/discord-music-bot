from pymongo import AsyncMongoClient
from dotenv import load_dotenv
import os, asyncio
from pydantic import BaseModel
from uuid import uuid4
from utils.models import Song, Favorite

load_dotenv()
DATABASE_URI = os.getenv("DATABASE_URI")
DATABASE_NAME = os.getenv('DATABASE_NAME')

client = AsyncMongoClient(DATABASE_URI)
db = client[DATABASE_NAME]
favorites_collection = db['favorites']

async def get_favorites(user_id: int) -> list:
    favorites = await favorites_collection.aggregate([
        {
            "$match": {
                "user_id": user_id 
            }
        },
        {
            "$project": {
                "_id": 1,
                "name": 1,
                "thumbnails": [
                    { "$ifNull": [ { "$arrayElemAt": ["$songs.thumbnail", 0] }, None ] },
                    { "$ifNull": [ { "$arrayElemAt": ["$songs.thumbnail", 1] }, None ] },
                    { "$ifNull": [ { "$arrayElemAt": ["$songs.thumbnail", 2] }, None ] },
                    { "$ifNull": [ { "$arrayElemAt": ["$songs.thumbnail", 3] }, None ] }
                ]
            }
        }
    ])

    return await favorites.to_list()

async def add_favorite(user_id, name, songs=[]) -> str:
    num = await favorites_collection.count_documents({'user_id': user_id})
    if num >= 10:
        raise Exception("You can only have 10 favorites")
    
    favorite = Favorite(
        id = str(uuid4()),
        user_id = user_id,
        name = name,
        songs = songs
    )
    save_data = favorite.model_dump()
    save_data['_id'] = save_data.pop('id')
    result = await favorites_collection.insert_one(save_data)
    return result.inserted_id

async def delete_favorite(user_id, favorite_id) -> int:
    result = await favorites_collection.delete_one({
        'user_id': user_id,
        '_id': favorite_id
    })


    return result.deleted_count

async def get_songs(user_id, favorite_id) -> tuple[str, list[Song]]:
    favorite = await favorites_collection.find_one({
        'user_id': user_id,
        '_id': favorite_id
    })
    
    if not favorite: raise Exception("Favorite not found")
    
    name = favorite.get('name', '')
    songs = favorite.get('songs', [])
    
    return name, songs

async def insert_song(user_id, favorite_id, song: Song):
    result = await favorites_collection.update_one(
        {
            'user_id': user_id,
            '_id': favorite_id
        },
        {
            '$addToSet': {
                'songs': song.model_dump()
            }
        }
    )
    
    return {'matched_count': result.matched_count, 'modified_count': result.modified_count}

async def remove_song(user_id, favorite_id, song_id):
    result = await favorites_collection.update_one(
        {
            'user_id': user_id,
            '_id': favorite_id,
        },
        {
            '$pull': {
                'songs': {
                    'id': song_id,
                }
            }
        }
    )
    
    return {'matched_count': result.matched_count, 'modified_count': result.modified_count}

async def main():
    pass
    
if __name__ == "__main__":
    asyncio.run(main())