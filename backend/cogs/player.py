import asyncio
from dotenv import load_dotenv
import os

import discord
from discord import app_commands
from discord.app_commands import Choice
from discord.ext import commands
from discord import VoiceClient, VoiceProtocol, Interaction

from utils.playback import play_song, pause_song, resume_song, skip_song
from utils.playing_list import Playlist, GuildPlaylistsManager
from utils.download import download_audio, search_yotube
from utils.auth_token import generate_token
from cogs.views import QueueView, SearchView

load_dotenv()
MANAGER_USER_ID = int(os.getenv("MANAGER_USER_ID"))

class MusicCog(commands.Cog):
    def __init__(self, bot: commands.Bot,  playlist_manager: GuildPlaylistsManager, *args, **kwargs):
        self.bot = bot
        self.queue = {}
        self.playlist_manager = playlist_manager

    async def check_user_voice(self, interaction: discord.Interaction):
        """ 檢查使用者是否在語音頻道 """
        # if interaction.user.id == MANAGER_USER_ID:
        #     return True
        if not interaction.user.voice or not interaction.user.voice.channel:
            await interaction.response.send_message("❌ 你需要先加入語音頻道才能使用這個指令！", ephemeral=True)
            return False
        return True
    
    async def get_voice_client(self, interaction: discord.Interaction):
        """ 獲取語音客戶端 """
        playlisyt = self.playlist_manager.get_playlist(interaction.guild_id, interaction.channel_id)
        if interaction.guild.voice_client is None:
            voice_channel = interaction.user.voice.channel
            voice_client = await voice_channel.connect(self_deaf=True)
        else:
            voice_client = interaction.guild.voice_client
            
        playlisyt.voice_client = voice_client
        return voice_client
    
    @app_commands.command(name = "hello", description = "Hello, world!")
    async def hello(self, interaction: Interaction):
        await interaction.response.send_message("Hello, world!")
        
    @app_commands.command(name = "test", description = "test")
    async def test(self, interaction: Interaction):
        playlisyt = self.playlist_manager.get_playlist(interaction.guild_id, interaction.channel_id)
        voice_client = await self.get_voice_client(interaction)
        
        print(interaction.guild.voice_client.channel)
        print(playlisyt.voice_client.channel)
        print([x.channel for x in self.bot.voice_clients])
        await interaction.response.send_message("test")

    
    @app_commands.command(name = 'join')
    async def join(self, interaction: Interaction):
        if not await self.check_user_voice(interaction):
            return
        
        voice_channel = interaction.user.voice.channel
        
        voice_client = await self.get_voice_client(interaction)
        if voice_client.channel != voice_channel:
            await voice_client.move_to(voice_channel)
            
        await interaction.response.send_message('連接至語音！')
        
    @app_commands.command(name = "leave", description = "leave")
    async def leave(self, interaction: Interaction):
        if not await self.check_user_voice(interaction):
            return

        if interaction.guild.voice_client:
            await interaction.guild.voice_client.disconnect()

        await interaction.response.send_message('中斷連接！')
            
    @app_commands.command(name = "play", description = "播放歌曲")
    @app_commands.describe(song = '輸入 YouTube 網址或關鍵字', choose = '選擇搜尋結果')
    @app_commands.choices(
        choose=[
            Choice(name="True", value=1),
            Choice(name="False", value=0),
        ]
    )
    async def play(self, interaction: Interaction, song: str, choose: Choice[int]=0):
        if not await self.check_user_voice(interaction):
            return
        await interaction.response.defer()

        
        playlist = self.playlist_manager.get_playlist(interaction.guild_id, interaction.channel_id)
        voice_client = await self.get_voice_client(interaction)
        
        if song.startswith('http'):
            await self.play_by_url(song, interaction, voice_client, playlist)
        else:
            await self.play_by_keyword(song, interaction, voice_client, playlist, choose)

    async def play_by_url(self, song_url: str, interaction: Interaction, voice_client: VoiceClient, playlist: Playlist):
        song_info = await download_audio(song_url)
        playlist.add_song(song_info)
        await interaction.followup.send(f'點播 {song_info["title"]}')
        
        play_song(self.bot, voice_client, playlist)
    
    async def play_by_keyword(self, keyword: str, interaction: Interaction, voice_client: VoiceClient, playlist: Playlist, choose: int):
        if not choose:
            result = await search_yotube(keyword)
            song = result[0]
            song_url = "https://www.youtube.com/watch?v=" + song['videoId']
            await self.play_by_url(song_url, interaction, voice_client, playlist)
        else:
            view = await SearchView.create(keyword, playlist)
            embed = view.create_embed()
            msg = await interaction.followup.send(embed=embed, view=view)
            view.message = msg
    
    
    @app_commands.command(name = "pause", description = "暫停播放")
    async def pause(self, interaction: Interaction):
        if not await self.check_user_voice(interaction):
            return
        
        voice_client = interaction.guild.voice_client
        pause_song(voice_client)
            
        await interaction.response.send_message('暫停播放')
    
    @app_commands.command(name = "resume", description = "回復播放")
    async def resume(self, interaction: Interaction):
        if not await self.check_user_voice(interaction):
            return
        
        voice_client = interaction.guild.voice_client
        if not voice_client.is_playing() and not voice_client.is_paused():
            playlist = self.playlist_manager.get_playlist(interaction.guild_id, interaction.channel_id)
            play_song(self.bot, voice_client, playlist)
        elif voice_client.is_paused():
            resume_song(voice_client)
        resume_song(voice_client)
            
        await interaction.response.send_message('回復播放')
        
    @app_commands.command(name = "skip", description = "跳過歌曲")
    async def skip(self, interaction: Interaction):
        if not await self.check_user_voice(interaction):
            return
        
        voice_client = interaction.guild.voice_client
        skip_song(voice_client)
        await interaction.response.send_message('跳過歌曲')
    
    @app_commands.command(name = "skipto", description = "跳至指定歌曲")
    async def skipto(self, interaction: Interaction, number: int):
        if not await self.check_user_voice(interaction):
            return
        
        playlist = self.playlist_manager.get_playlist(interaction.guild_id)
        song = playlist.skip_to(number-1)
        if song:
            voice_client = interaction.guild.voice_client
            if voice_client and voice_client.is_playing():
                voice_client.stop()
            await interaction.response.send_message(f'跳至-> {song["title"]} <-')

    @app_commands.command(name = "remove", description = "刪除曲目")
    async def remove(self, interaction: Interaction, number: int):
        if not await self.check_user_voice(interaction):
            return
        
        playlist = self.playlist_manager.get_playlist(interaction.guild_id)
        song = playlist.remove_song(number-1)
        if song:
            await interaction.response.send_message(f'刪除-> {song["title"]} <-成功')

    @app_commands.command(name = "clear", description = "清空曲目")
    async def clear(self, interaction: Interaction):
        if not await self.check_user_voice(interaction):
            return
        
        self.playlist_manager.clear_playlist(interaction.guild_id)
        await interaction.response.send_message(f'清空曲目')
    
    @app_commands.command(name = "loop", description = "循環播放、再次播放")
    async def loop(self, interaction: Interaction):
        if not await self.check_user_voice(interaction):
            return
        
        playlist = self.playlist_manager.get_playlist(interaction.guild_id)
        loop = not playlist.loop_queue
        playlist.loop_queue = loop
        
        if loop:
            voice_client = await self.get_voice_client(interaction)
            play_song(self.bot, voice_client, playlist)
        await interaction.response.send_message(f'循環播放: {loop}')
        
    @app_commands.command(name = "info", description = "當前曲目")
    async def info(self, interaction: Interaction):
        if not await self.check_user_voice(interaction):
            return
        
        playlist = self.playlist_manager.get_playlist(interaction.guild_id)
        song = playlist.current_info()
        if song:
            await interaction.response.send_message(f'正在撥放-> {song["title"]} <-')
                    
    @app_commands.command(name = "queue", description = "queue")
    async def queue(self, interaction: Interaction):
        if not await self.check_user_voice(interaction):
            return
        
        playlist = self.playlist_manager.get_playlist(interaction.guild_id)
        songs, current_index = playlist.view_playlist()
        
        view = QueueView(songs, current_index)
        embed = view.create_embed()

        await interaction.response.send_message(embed=embed, view=view)

    @commands.Cog.listener()
    async def on_voice_state_update(self, member: discord.Member, before, after):
        voice_client = discord.utils.get(self.bot.voice_clients, guild=member.guild)
        if voice_client and len(voice_client.channel.members) == 1:
            await asyncio.sleep(60)
            voice_client = discord.utils.get(self.bot.voice_clients, guild=member.guild)
            if voice_client and len(voice_client.channel.members) == 1:
                self.playlist_manager.remove_guild(member.guild.id)
                voice_client.stop()
                await voice_client.disconnect()


    @app_commands.command(name = "web", description = "web")
    async def web(self, interaction: Interaction):
        if not await self.check_user_voice(interaction):
            return
        voice_client = await self.get_voice_client(interaction)
        token = generate_token(interaction.guild_id, interaction.channel_id, interaction.user.id)
        url = f"http://localhost:8000/auth/set/?token={token}"
        await interaction.response.send_message(url, ephemeral=True, delete_after=30)
