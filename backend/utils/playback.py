import asyncio, logging
from discord import FFmpegOpusAudio, VoiceClient, Embed
from discord.ext.commands import Bot
from utils.playing_list import Playlist

logger = logging.getLogger("app")

async def play_next(bot: Bot, voice_client: VoiceClient, playlist: Playlist):
    FFMPEG_OPTIONS = {
        'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5 -nostdin',
        'options': '-vn -bufsize 64k -loglevel quiet'
    }
    
    song = playlist.next_song()
    if song:
        source = await FFmpegOpusAudio.from_probe(song['source'], **FFMPEG_OPTIONS)
        embed = Embed(title=song['title'], url=song['webpage_url'])
        embed.set_author(name=song['channel'], url=song['channel_url'])
        embed.set_thumbnail(url=song['thumbnail'])
        await bot.get_channel(playlist.channel_id).send(embed=embed)
        
        voice_client.play(source, after=lambda e: play_song(bot, voice_client, playlist, e))
        
def play_song(bot: Bot, voice_client: VoiceClient, playlist: Playlist, e = None):
    logger.debug(f"Attempt to play song, voice_client: {voice_client.guild}, is_playing: {voice_client.is_playing()}, is_paused: {voice_client.is_paused()}")
    if e: logger.error(e)
    if not voice_client.is_playing() and not voice_client.is_paused():
        bot.loop.create_task(play_next(bot, voice_client, playlist))
        
def pause_song(voice_client: VoiceClient):
    logger.debug(f"Pausing song, voice_client: {voice_client.guild}, is_playing: {voice_client.is_playing()}, is_paused: {voice_client.is_paused()}")
    if voice_client and voice_client.is_playing():
        voice_client.pause()
        
def resume_song(voice_client: VoiceClient):
    logger.debug(f"Resuming song, voice_client: {voice_client.guild}, is_playing: {voice_client.is_playing()}, is_paused: {voice_client.is_paused()}")
    if voice_client and voice_client.is_paused():
        voice_client.resume()
        
def skip_song(voice_client: VoiceClient):
    logger.debug(f"Skipping song, voice_client: {voice_client.guild}, is_playing: {voice_client.is_playing()}, is_paused: {voice_client.is_paused()}")
    if voice_client and voice_client.is_playing():
        voice_client.stop()