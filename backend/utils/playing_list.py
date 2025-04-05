from discord import VoiceClient, VoiceProtocol
from typing import Union

class Playlist:
    def __init__(self, channel_id: str, voice_client: Union[VoiceClient, VoiceProtocol] = None):
        self.songs = []
        self.channel_id = channel_id
        self.loop_queue = False
        self.current_index = -1 # 第 {current_index + 1} 首歌
        self.voice_client: VoiceClient = None 

    def add_song(self, song: dict):
        self.songs.append(song)

    def remove_song(self, index: int):     
        if 0 <= index < len(self.songs):
            if index < self.current_index:
                self.current_index -= 1 
                
            song = self.songs[index]
            del self.songs[index] 
            return song
        
    def next_song(self):
        if not self.is_empty():
            if self.is_end():
                if self.loop_queue: 
                    self.reset_index()
                else:
                    return None
            self.current_index += 1
            song = self.songs[self.current_index]
            return song
        return None
    
    def is_end(self):
        return self.current_index + 1 >= len(self.songs)

    def is_empty(self):
        return len(self.songs) == 0

    def reset_index(self):
        self.current_index = -1
        
    def clear(self):
        self.songs.clear()
        self.current_index = 0

    def view_playlist(self):
        return self.songs, self.current_index
    
    def current_info(self):
        if 0 <= self.current_index < len(self.songs):
            return self.songs[self.current_index]
    
    def skip_to(self, index: int):
        if 0 <= index < len(self.songs):
            self.current_index = index-1
            return self.songs[index]

class GuildPlaylistsManager:
    def __init__(self):
        self.guild_playlists = {}

    def get_playlist(self, guild_id: int, channel_id: int= None) -> Playlist:
        """取得該伺服器的播放清單，若無則創建新的"""
        if guild_id not in self.guild_playlists:
            self.guild_playlists[guild_id] = Playlist(channel_id)
        return self.guild_playlists[guild_id]

    def clear_playlist(self, guild_id: int):
        """清空該伺服器的播放清單"""
        if guild_id in self.guild_playlists:
            self.guild_playlists[guild_id].clear()

    def remove_guild(self, guild_id: int):
        """當伺服器不再使用音樂機器人時移除該伺服器的播放清單"""
        if guild_id in self.guild_playlists:
            del self.guild_playlists[guild_id]