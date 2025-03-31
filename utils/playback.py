import asyncio
from discord import FFmpegOpusAudio, VoiceClient, Embed
from discord.ext.commands import Bot
from utils.playing_list import Playlist

async def play_next(bot: Bot, voice_client: VoiceClient, playlist: Playlist):
    FFMPEG_OPTIONS = {
        'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
        'options': '-vn'
    }
    
    song = playlist.next_song()
    if song:
        source = await FFmpegOpusAudio.from_probe(song['source'], **FFMPEG_OPTIONS)
        embed = Embed(title=song['title'], url=song['webpage_url'])
        embed.set_author(name=song['channel'], url=song['channel_url'])
        embed.set_thumbnail(url=song['thumbnail'])
        await bot.get_channel(playlist.channel_id).send(embed=embed)
        
        voice_client.play(source, after=lambda e: play_song(bot, voice_client, playlist))
    else:
        await asyncio.sleep(30)
        if not voice_client.is_playing() and voice_client.is_connected():
            await voice_client.disconnect()
        
def play_song(bot: Bot, voice_client: VoiceClient, playlist: Playlist):
    if not voice_client.is_playing() and not voice_client.is_paused():
        bot.loop.create_task(play_next(bot, voice_client, playlist))
        
def pause_song(voice_client: VoiceClient):
    if voice_client and voice_client.is_playing():
        voice_client.pause()
        
def resume_song(voice_client: VoiceClient):
    if voice_client and voice_client.is_paused():
        voice_client.resume()
        
def skip_song(voice_client: VoiceClient):
    if voice_client and voice_client.is_playing():
        voice_client.stop()