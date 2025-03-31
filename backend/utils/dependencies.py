from fastapi import HTTPException, WebSocketException, Request, status, WebSocket, Depends
import asyncio
import discord.utils
from discord.ext.commands import Bot
from utils.playing_list import GuildPlaylistsManager, Playlist
from typing import Union

async def check_session(websocket: WebSocket= None, request: Request= None) -> dict:
    session = websocket.session if websocket else request.session
    guild_id = session.get("guild_id")
    channel_id = session.get("channel_id")
    user_id = session.get("user_id")
    if not guild_id or not channel_id or not user_id:
        raise HTTPException(status_code=401, detail="Session values missing")

    return session

async def get_user_voice_channel(websocket: WebSocket= None, request: Request= None, session= Depends(check_session)) -> discord.VoiceChannel:
    app = websocket.app if websocket else request.app
    guild_id = session.get("guild_id")
    user_id = session.get("user_id")

    bot: Bot = app.state.bot
    guild = bot.get_guild(guild_id)
    voice_state = guild.get_member(user_id).voice if guild else None
    voice_channel = voice_state.channel if voice_state else None
    if not voice_channel:
        raise HTTPException(status_code=404, detail="請先加入語音頻道")


    return voice_channel

async def get_playlist(websocket: WebSocket= None, request: Request= None, voice_channel= Depends(get_user_voice_channel), session= Depends(check_session)) -> Playlist:
    app = websocket.app if websocket else request.app
    guild_id = session.get("guild_id")
    channel_id = session.get("channel_id")
        
    playlist: Playlist = app.state.playlist_manager.get_playlist(guild_id, channel_id)
    bot: Bot = app.state.bot
    guild = bot.get_guild(guild_id)
    if guild.voice_client is None:
        future = asyncio.run_coroutine_threadsafe(voice_channel.connect(self_deaf=True), bot.loop)
        voice_client = future.result()
    else:
        voice_client = guild.voice_client

    playlist.voice_client = voice_client
    return playlist