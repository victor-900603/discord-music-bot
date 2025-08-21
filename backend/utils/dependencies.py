from fastapi import HTTPException, Request, WebSocket, Depends
import asyncio
import discord
from discord.ext.commands import Bot
from utils.playing_list import Playlist

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
    guild = bot.get_guild(session["guild_id"])
    if not guild:
        raise HTTPException(status_code=404, detail="找不到伺服器")
    
    member = guild.get_member(session["user_id"])
    if not member or not member.voice:
        session.pop("guild_id", None)
        session.pop("channel_id", None)
        session.pop("user_id", None)
        raise HTTPException(status_code=404, detail="請先加入語音頻道並重新連接")

    return member.voice.channel

async def get_playlist(websocket: WebSocket= None, request: Request= None, voice_channel= Depends(get_user_voice_channel), session= Depends(check_session)) -> Playlist:
    app = websocket.app if websocket else request.app
    guild_id = session.get("guild_id")
    channel_id = session.get("channel_id")
        
    playlist: Playlist = app.state.playlist_manager.get_playlist(guild_id, channel_id)
    bot: Bot = app.state.bot
    guild = bot.get_guild(guild_id)
    if guild.voice_client is None:
        voice_client = await voice_channel.connect(self_deaf=True)
    else:
        voice_client = guild.voice_client

    playlist.voice_client = voice_client
    return playlist