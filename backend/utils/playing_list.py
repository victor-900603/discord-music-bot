import random
from discord import VoiceClient, VoiceProtocol
from typing import Union, List, Optional, Tuple, Dict, Any

class Playlist:
    """伺服器播放列表，管理歌曲佇列、播放狀態與循環/隨機等設定"""
    
    DEFAULT_VOLUME = 0.5
    MIN_VOLUME = 0.0
    MAX_VOLUME = 1.0

    def __init__(self, channel_id: str, voice_client: Union[VoiceClient, VoiceProtocol] = None):
        self.songs: List[Dict] = []
        self.channel_id = channel_id
        self.loop_queue: bool = False
        self.shuffle: bool = False
        self.volume: float = self.DEFAULT_VOLUME
        self.current_index: int = -1  # 第 {current_index + 1} 首歌
        self.voice_client: Optional[VoiceClient] = None
        self._shuffle_order: List[int] = []
        self._shuffle_position: int = -1

    def add_song(self, song: dict):
        """
        將歌曲加入播放列表
        
        :param song: 歌曲資訊字典
        """
        self.songs.append(song)
        if self.shuffle:
            self._shuffle_order.append(len(self.songs) - 1)

    def add_songs(self, songs: list[dict]):
        """
        批量加入歌曲到播放列表
        
        :param songs: 歌曲資訊字典列表
        """
        for song in songs:
            self.add_song(song)

    def remove_song(self, index: int):     
        """
        移除指定索引的歌曲

        :param index: 要移除歌曲的索引（0-based）
        :return: 被移除的歌曲資訊，若索引無效返回 None
        """
        if 0 <= index < len(self.songs):
            if index < self.current_index:
                self.current_index -= 1 
            elif index == self.current_index:
                pass
                
            song = self.songs[index]
            del self.songs[index]

            if self.shuffle:
                self._rebuild_shuffle_order()
            return song
        return None

    def move_song(self, from_index: int, to_index: int) -> bool:
        """
        移動歌曲到指定位置
        
        :param from_index: 原始位置索引（0-based）
        :param to_index: 目標位置索引（0-based）
        :return: 是否成功移動
        """
        if not (0 <= from_index < len(self.songs) and 0 <= to_index < len(self.songs)):
            return False
        
        song = self.songs.pop(from_index)
        self.songs.insert(to_index, song)
        
        if from_index == self.current_index:
            self.current_index = to_index
        elif from_index < self.current_index <= to_index:
            self.current_index -= 1
        elif to_index <= self.current_index < from_index:
            self.current_index += 1
        
        return True
        
    def next_song(self):
        """取得下一首歌曲，支援隨機播放模式"""
        if self.is_empty():
            return None
        
        if self.shuffle:
            return self._next_shuffle_song()
        
        if self.is_end():
            if self.loop_queue: 
                self.reset_index()
            else:
                return None
        self.current_index += 1
        return self.songs[self.current_index]
    
    def _next_shuffle_song(self):
        """隨機播放模式下取得下一首"""
        if not self._shuffle_order:
            self._rebuild_shuffle_order()
        
        self._shuffle_position += 1
        if self._shuffle_position >= len(self._shuffle_order):
            if self.loop_queue:
                self._rebuild_shuffle_order()
                self._shuffle_position = 0
            else:
                return None
        
        self.current_index = self._shuffle_order[self._shuffle_position]
        return self.songs[self.current_index]

    def _rebuild_shuffle_order(self):
        """重建隨機播放順序"""
        self._shuffle_order = list(range(len(self.songs)))
        random.shuffle(self._shuffle_order)
        self._shuffle_position = -1

    def toggle_shuffle(self) -> bool:
        """切換隨機播放模式，返回新的狀態"""
        self.shuffle = not self.shuffle
        if self.shuffle:
            self._rebuild_shuffle_order()
        else:
            self._shuffle_order.clear()
            self._shuffle_position = -1
        return self.shuffle

    def set_volume(self, volume: float) -> float:
        """
        設定音量
        
        :param volume: 音量值 (0.0 ~ 1.0)
        :return: 實際設定的音量值
        """
        self.volume = max(self.MIN_VOLUME, min(self.MAX_VOLUME, volume))
        # 即時調整正在播放的音源音量
        if (self.voice_client 
            and self.voice_client.source 
            and hasattr(self.voice_client.source, 'volume')):
            self.voice_client.source.volume = self.volume
        return self.volume

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
        """清空播放列表並重置所有狀態"""
        self.songs.clear()
        self.current_index = -1
        self._shuffle_order.clear()
        self._shuffle_position = -1

    def view_playlist(self):
        """查看播放列表與當前索引"""
        return self.songs, self.current_index
    
    def current_info(self):
        """取得當前正在播放的歌曲資訊"""
        if 0 <= self.current_index < len(self.songs):
            return self.songs[self.current_index]
        return None
    
    def skip_to(self, index: int):
        """
        跳至指定歌曲
        
        :param index: 0-based，會把 current_index 設為前一首，以便播放指定歌曲
        :return: 目標歌曲資訊，若索引無效返回 None
        """
        if 0 <= index < len(self.songs):
            self.current_index = index - 1
            return self.songs[index]
        return None

    @property
    def length(self) -> int:
        """返回播放列表長度"""
        return len(self.songs)


class GuildPlaylistsManager:
    """全域伺服器播放列表管理員，管理所有 Guild 的播放列表實例"""

    def __init__(self):
        self.guild_playlists: Dict[int, Playlist] = {}

    def get_playlist(self, guild_id: int, channel_id: int = None) -> Playlist:
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

    def get_all_guilds(self) -> list[int]:
        """取得所有正在使用的伺服器 ID"""
        return list(self.guild_playlists.keys())