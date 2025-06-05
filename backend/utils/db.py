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

async def get_favorites(user_id: int) -> list[Favorite]:
    favorites = favorites_collection.find({"user_id": user_id})

    return await favorites.to_list()


async def add_favorite(user_id, name, songs=[]) -> str:
    num = await favorites_collection.count_documents({'user_id': user_id})
    if num >= 5:
        raise Exception("You can only have 5 favorites")
    
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

async def get_songs(user_id, favorite_id) -> list[Song]:
    favorite = await favorites_collection.find_one({
        'user_id': user_id,
        '_id': favorite_id
    })
    
    if not favorite: raise Exception("Favorite not found")
    
    songs = favorite.get('songs', [])
    
    return songs

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

    # print(await insert_favorite(123, '456'))
    # print(await favorites_collection.count_documents({'user_id': 123}))
    # print(await get_favorites(123))
    # print(await delete_favorite(123, '627f13f0-03ce-4bca-98a7-288396d699cb'))
    
    # print(await insert_song(123, '6dfa4173-9f53-4fe0-9e20-3094939bebb3', Song(
    #     id='qwerqq1111',
    #     title="Test",
    #     channel="Test",
    #     thumbnail="Testa"
    # )))
    matched_count, modified_count = (await insert_song(123, '6dfa4173-9f53-4fe0-9e20-3094939bebb3', Song(
        id='qwerqq1111',
        title="Test",
        channel="Test",
        thumbnail="Testa"
    ))).values()
    print(matched_count)
    # print(await remove_song(123, '6dfa4173-9f53-4fe0-9e20-3094939bebb3', '5510bbe7-9952-4a10-97ad-7904e2fc1e51'))
    
    # print(Song(
    #     id='qwer',
    #     title="Test",
    #     channel="Test",
    #     thumbnail="Test"
    # ))
    
    # d = {
    #     'source': 's',
    #     'title': 't',
    #     'webpage_url': 'w',
    #     'thumbnail': 't',
    #     'channel': 'v',
    #     'channel_url': 'v'
    # }
    # print(Song(d))
if __name__ == "__main__":
    asyncio.run(main())
