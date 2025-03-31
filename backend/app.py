import discord
from discord.ext import commands

from cogs import MusicCog
from utils.playing_list import GuildPlaylistsManager

from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware
from starlette.middleware.cors import CORSMiddleware

import uvicorn
from router import auth_router, search_router, playlist_router, playback_router

import json
import os, sys, time
import asyncio
from threading import Thread
from dotenv import load_dotenv
import logging
from uvicorn.config import LOGGING_CONFIG



load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

playlist_manager = GuildPlaylistsManager()


intents = discord.Intents.all()  # 機器人的意圖 all/default/none
intents.message_content = True
bot = commands.Bot(command_prefix='?', intents=intents)
def bot_server():
    async def load_cogs():
        await bot.load_extension("cogs.general")
        await bot.add_cog(MusicCog(bot, playlist_manager))
        
    asyncio.run(load_cogs())
    bot.run(DISCORD_TOKEN)

app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key='')
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"], 
#     allow_credentials=True,
#     allow_methods=["*"], 
#     allow_headers=["*"], 
# )
app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(search_router, prefix="/search", tags=["search"])
app.include_router(playlist_router, prefix="/playlist", tags=["playlist"])
app.include_router(playback_router, prefix="/playback", tags=["playback"])
def api_server():
    app.state.bot = bot
    app.state.playlist_manager = playlist_manager
    uvicorn.run(app, host="localhost", port=8000)

def setup_logging():
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    # 設置 FastAPI 的 log
    LOGGING_CONFIG["formatters"]["default"]["fmt"] = "%(asctime)s - %(levelprefix)s %(message)s"
    LOGGING_CONFIG["formatters"]["access"]["fmt"] = "%(asctime)s - %(levelprefix)s %(client_addr)s - \"%(request_line)s\" %(status_code)s"
    
    # 設置 Discord 機器人的 log
    discord_logger = logging.getLogger("discord")
    discord_logger.setLevel(logging.INFO)
    discord_handler = logging.StreamHandler()
    discord_handler.setFormatter(formatter)
    discord_logger.addHandler(discord_handler)


if __name__ == "__main__":
    setup_logging()

    api_thread = Thread(target=api_server)
    api_thread.daemon = True
    bot_thread = Thread(target=bot_server)
    bot_thread.daemon = True
    
    api_thread.start()
    bot_thread.start()
	
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("程序中斷，正在退出...")
        sys.exit(0)
