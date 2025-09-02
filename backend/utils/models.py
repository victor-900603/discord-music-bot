from pydantic import BaseModel

class Song(BaseModel):
    id: str
    title: str
    channel: str
    thumbnail: str

class Favorite(BaseModel):
    id: str
    user_id: int
    name: str
    songs: list[Song]
    
class Token(BaseModel):
    token: str