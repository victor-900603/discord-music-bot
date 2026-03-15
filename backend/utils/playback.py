import asyncio
import logging
from discord import FFmpegOpusAudio, PCMVolumeTransformer, VoiceClient, Embed
from discord.ext.commands import Bot
from utils.playing_list import Playlist

logger = logging.getLogger("app")

FFMPEG_OPTIONS = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5 -nostdin',
    'options': '-vn -bufsize 64k -loglevel quiet'
}


async def play_next(bot: Bot, voice_client: VoiceClient, playlist: Playlist):
    """異步取得下一首歌曲並開始播放"""
    song = playlist.next_song()
    if song is None:
        return
    
    try:
        source = await FFmpegOpusAudio.from_probe(song['source'], **FFMPEG_OPTIONS)
    except Exception as e:
        logger.error(f"無法播放歌曲 '{song.get('title', 'Unknown')}': {e}")
        play_song(bot, voice_client, playlist)
        return
    
    try:
        embed = Embed(title=song['title'], url=song['webpage_url'])
        embed.set_author(name=song['channel'], url=song['channel_url'])
        embed.set_thumbnail(url=song['thumbnail'])
        channel = bot.get_channel(playlist.channel_id)
        if channel:
            await channel.send(embed=embed)
    except Exception as e:
        logger.warning(f"無法發送播放訊息: {e}")
    
    voice_client.play(
        source, 
        after=lambda e: play_song(bot, voice_client, playlist, e)
    )


def play_song(bot: Bot, voice_client: VoiceClient, playlist: Playlist, error=None):
    """觸發播放下一首歌曲（會檢查目前是否已在播放）"""
    logger.debug(
        f"Attempt to play song, guild: {voice_client.guild}, "
        f"is_playing: {voice_client.is_playing()}, "
        f"is_paused: {voice_client.is_paused()}"
    )
    if error:
        logger.error(f"播放錯誤: {error}")
    if not voice_client.is_playing() and not voice_client.is_paused():
        bot.loop.create_task(play_next(bot, voice_client, playlist))


def pause_song(voice_client: VoiceClient):
    """暫停目前播放的歌曲"""
    logger.debug(
        f"Pausing song, guild: {voice_client.guild}, "
        f"is_playing: {voice_client.is_playing()}"
    )
    if voice_client and voice_client.is_playing():
        voice_client.pause()


def resume_song(voice_client: VoiceClient):
    """恢復暫停的歌曲"""
    logger.debug(
        f"Resuming song, guild: {voice_client.guild}, "
        f"is_paused: {voice_client.is_paused()}"
    )
    if voice_client and voice_client.is_paused():
        voice_client.resume()


def skip_song(voice_client: VoiceClient):
    """跳過目前歌曲（觸發 after callback 播放下一首）"""
    logger.debug(
        f"Skipping song, guild: {voice_client.guild}, "
        f"is_playing: {voice_client.is_playing()}"
    )
    if voice_client and (voice_client.is_playing() or voice_client.is_paused()):
        voice_client.stop()