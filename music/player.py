import asyncio
import discord
from discord import app_commands
from discord.ext import commands
from discord import VoiceClient, VoiceProtocol, Interaction
from music.playlist import Playlist, GuildPlaylistsManager
from music.ui import QueueView, SearchView
from music.utils.download import download_audio


class Music_bot(commands.Cog):
    def __init__(self, bot: commands.Bot,  playlist_manager: GuildPlaylistsManager, *args, **kwargs):
        self.bot = bot
        self.queue = {}
        self.playlist_manager = playlist_manager


    @app_commands.command(name = "hello", description = "Hello, world!")
    async def hello(self, interaction: Interaction):
        await interaction.response.send_message("Hello, world!")
        
    @app_commands.command(name = "test", description = "test")
    async def test(self, interaction: Interaction):
        print([x for x in self.bot.get_all_channels()])
    
    @app_commands.command(name = 'join')
    async def join(self, interaction: Interaction):
        if not interaction.user.voice:
            await interaction.response.send_message('請連接至語音頻道！')
            return
        voice_channel = interaction.user.voice.channel
        if interaction.guild.voice_client is None:
            await voice_channel.connect(self_deaf=True)
        else:
            await interaction.guild.voice_client.move_to(voice_channel)
        await interaction.response.send_message('連接至語音！')
        
    @app_commands.command(name = "leave", description = "leave")
    async def leave(self, interaction: Interaction):
        if not interaction.user.voice:
            await interaction.response.send_message('請連接至語音頻道！')
            return
    
        await interaction.guild.voice_client.disconnect()
        await interaction.response.send_message('中斷連接！')
        
    @app_commands.command(name = "play", description = "播放歌曲")
    @app_commands.describe(song = '輸入 YouTube 網址或關鍵字')
    async def play(self, interaction: Interaction, song: str):
        if not interaction.user.voice:
            await interaction.response.send_message('請連接至語音頻道！')
            return
        
        if interaction.guild.voice_client is None:
            voice_channel = interaction.user.voice.channel
            voice_client = await voice_channel.connect(self_deaf=True)
        else:
            voice_client = interaction.guild.voice_client
        
        playlist = self.playlist_manager.get_playlist(interaction.guild_id, interaction.channel_id)
        await interaction.response.defer()
        
        if song.startswith('http'):
            await self.play_by_url(song, interaction, voice_client, playlist)
        else:
            await self.play_by_keyword(song, interaction, voice_client, playlist)

    async def play_by_url(self, song: str, interaction: Interaction, voice_client: VoiceClient, playlist: Playlist):
        song_info = download_audio(song)
        playlist.add_song(song_info)
        await interaction.followup.send(f'點播 {song_info["title"]}')
        
        if not voice_client.is_playing() and not voice_client.is_paused():
            self.bot.loop.create_task(self.play_next(voice_client, playlist))
    
    async def play_by_keyword(self, song: str, interaction: Interaction, voice_client: VoiceClient, playlist: Playlist):
        view = SearchView(song, playlist, self)
        embed = view.create_embed()
        msg = await interaction.followup.send(embed=embed, view=view)
        view.message = msg

    
    async def play_next(self, voice_client: VoiceClient, playlist: Playlist):
        FFMPEG_OPTIONS = {
            'before_options':
            '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
            'options': '-vn'
        }
        song = playlist.next_song()
        if song:
            source = await discord.FFmpegOpusAudio.from_probe(song['source'], **FFMPEG_OPTIONS)
            embed = discord.Embed(title=song['title'], url=song['webpage_url'])
            embed.set_author(name=song['channel'], url=song['channel_url'])
            embed.set_thumbnail(url=song['thumbnail'])
            await self.bot.get_channel(playlist.channel_id).send(embed=embed)
            
            voice_client.play(source, after=lambda e: self.play_after(voice_client, playlist))
        else:
            await asyncio.sleep(30)
            if not voice_client.is_playing() and voice_client.is_connected():
                await voice_client.disconnect()
            
    def play_after(self, voice_client: VoiceClient, playlist: Playlist):
        self.bot.loop.create_task(self.play_next(voice_client, playlist))
    
    
    @app_commands.command(name = "pause", description = "暫停播放")
    async def pause(self, interaction: Interaction):
        voice_client = interaction.guild.voice_client
        if voice_client and voice_client.is_playing():
            voice_client.pause()
        await interaction.response.send_message('暫停播放')
    
    @app_commands.command(name = "resume", description = "回復播放")
    async def resume(self, interaction: Interaction):
        voice_client = interaction.guild.voice_client
        if voice_client and voice_client.is_paused():
            voice_client.resume()
        await interaction.response.send_message('回復播放')
        
    @app_commands.command(name = "skip", description = "跳過歌曲")
    async def skip(self, interaction: Interaction):
        voice_client = interaction.guild.voice_client
        if voice_client and voice_client.is_playing():
            voice_client.stop()
        await interaction.response.send_message('跳過歌曲')
    
    @app_commands.command(name = "skipto", description = "跳至指定歌曲")
    async def skipto(self, interaction: Interaction, index: int):
        playlist = self.playlist_manager.get_playlist(interaction.guild_id)
        song = playlist.skip_to(index-1)
        if song:
            voice_client = interaction.guild.voice_client
            if voice_client and voice_client.is_playing():
                voice_client.stop()
            await interaction.response.send_message(f'跳至-> {song["title"]} <-')

    @app_commands.command(name = "remove", description = "刪除曲目")
    async def remove(self, interaction: Interaction, index: int):
        playlist = self.playlist_manager.get_playlist(interaction.guild_id)
        song = playlist.remove_song(index-1)
        if song:
            await interaction.response.send_message(f'刪除-> {song["title"]} <-成功')

    @app_commands.command(name = "clear", description = "清空曲目")
    async def clear(self, interaction: Interaction):
        playlist = self.playlist_manager.get_playlist(interaction.guild_id)
        playlist.clear()
        await interaction.response.send_message(f'清空曲目')
    
    @app_commands.command(name = "loop", description = "循環播放")
    async def loop(self, interaction: Interaction):
        playlist = self.playlist_manager.get_playlist(interaction.guild_id)
        loop = not playlist.loop_queue
        playlist.loop_queue = loop
        await interaction.response.send_message(f'循環播放: {loop}')
        
    @app_commands.command(name = "info", description = "當前曲目")
    async def info(self, interaction: Interaction):
        playlist = self.playlist_manager.get_playlist(interaction.guild_id)
        song = playlist.current_info()
        if song:
            await interaction.response.send_message(f'正在撥放-> {song["title"]} <-')
                    
    @app_commands.command(name = "queue", description = "queue")
    async def queue(self, interaction: Interaction):
        playlist = self.playlist_manager.get_playlist(interaction.guild_id)
        songs, current_index = playlist.view_playlist()
        
        view = QueueView(songs, current_index)
        embed = view.create_embed()

        await interaction.response.send_message(embed=embed, view=view)

    @commands.Cog.listener()
    async def on_voice_state_update(self, member: discord.Member, before, after):
        voice_client = discord.utils.get(self.bot.voice_clients, guild=member.guild)
        
        if voice_client and len(voice_client.channel.members) == 1:
            playlist = self.playlist_manager.get_playlist(member.guild.id)
            playlist.clear()
            voice_client.stop()
            await voice_client.disconnect()
