from discord import VoiceClient, VoiceProtocol
from typing import Union, List, Optional, Tuple, Dict, Any

class Playlist:
    def __init__(self, channel_id: str, voice_client: Union[VoiceClient, VoiceProtocol] = None):
        self.songs: List[Dict] = []
        self.channel_id = channel_id
        self.loop_queue: bool = False
        self.current_index:int = -1 # 第 {current_index + 1} 首歌
        self.voice_client: Optional[VoiceClient] = None 

    def add_song(self, song: dict):
        """
        將歌曲加入播放列表
        
        :param song: 歌曲資訊字典
        """
        self.songs.append(song)

    def remove_song(self, index: int):     
        """
        移除指定索引的歌曲

        :param index: 要移除歌曲的索引（0-based）
        """
        if 0 <= index < len(self.songs):
            if index < self.current_index:
                self.current_index -= 1 
                
            song = self.songs[index]
            del self.songs[index] 
            return song
        
    def next_song(self):
        """取得下一首歌曲"""
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
        """判斷播放列表是否到尾端"""
        return self.current_index + 1 >= len(self.songs)

    def is_empty(self):
        """判斷播放列表是否為空"""
        return len(self.songs) == 0

    def reset_index(self):
        """將播放索引重置為 -1"""
        self.current_index = -1
        
    def clear(self):
        """清空播放列表並重置索引"""
        self.songs.clear()
        self.current_index = -1

    def view_playlist(self):
        """查看播放列表與當前索引"""
        return self.songs, self.current_index
    
    def current_info(self):
        """取得當前正在播放的歌曲資訊"""
        if 0 <= self.current_index < len(self.songs):
            return self.songs[self.current_index]
    
    def skip_to(self, index: int):
        """
        跳至指定歌曲
        index: 0-based，會把 current_index 設為前一首，以便播放指定歌曲
        """
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