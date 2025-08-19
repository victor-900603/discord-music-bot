# app.py
import os
import asyncio
import discord
from discord.ext import commands
from dotenv import load_dotenv

from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware
from starlette.middleware.cors import CORSMiddleware
import uvicorn
import logging
from uvicorn.config import LOGGING_CONFIG
import copy

from cogs import MusicCog
from utils.playing_list import GuildPlaylistsManager
from router import auth_router, search_router, playlist_router, playback_router, favorites_router

load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
SESSION_SECRET = os.getenv("SESSION_SECRET", "default_secret")

playlist_manager = GuildPlaylistsManager()

# ---------------- Logging 設定 ----------------
def setup_logging():
    # Discord 日誌
    discord_logger = logging.getLogger("discord")
    discord_logger.setLevel(logging.INFO)
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    ch = logging.StreamHandler()
    ch.setFormatter(formatter)
    discord_logger.addHandler(ch)

    # FastAPI/Uvicorn 日誌
    log_config = copy.deepcopy(LOGGING_CONFIG)
    log_config["formatters"]["default"]["fmt"] = "%(asctime)s - %(levelprefix)s %(message)s"
    log_config["formatters"]["access"]["fmt"] = "%(asctime)s - %(levelprefix)s %(client_addr)s - \"%(request_line)s\" %(status_code)s"
    return log_config

# ---------------- Discord Bot ----------------
intents = discord.Intents.all()
intents.message_content = True
bot = commands.Bot(command_prefix="?", intents=intents)

@bot.event
async def on_ready():
    print(f"已登入 Discord：{bot.user}")

async def load_cogs():
    await bot.load_extension("cogs.general")
    await bot.add_cog(MusicCog(bot, playlist_manager))

# ---------------- FastAPI ----------------
app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key=SESSION_SECRET)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
)
app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(search_router, prefix="/search", tags=["search"])
app.include_router(playlist_router, prefix="/playlist", tags=["playlist"])
app.include_router(playback_router, prefix="/playback", tags=["playback"])
app.include_router(favorites_router, prefix="/favorites", tags=["favorites"])

app.state.bot = bot
app.state.playlist_manager = playlist_manager

# ---------------- 主執行 ----------------
async def main():
    await load_cogs()

    bot_task = asyncio.create_task(bot.start(DISCORD_TOKEN))

    log_config = setup_logging()
    api_config = uvicorn.Config(app, host="127.0.0.1", port=8000, log_config=log_config)
    api_server = uvicorn.Server(api_config)
    api_task = asyncio.create_task(api_server.serve())

    await asyncio.gather(bot_task, api_task)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("程序中斷，正在退出...")
