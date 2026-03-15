# app.py
import os
import asyncio
import discord
from discord.ext import commands
from dotenv import load_dotenv

from fastapi import FastAPI, Request, HTTPException, status
from fastapi.responses import JSONResponse
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
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:5173")
API_HOST = os.getenv("API_HOST", "127.0.0.1")
API_PORT = int(os.getenv("API_PORT", "8000"))

playlist_manager = GuildPlaylistsManager()

# ---------------- Logging 設定 ----------------
def setup_logging():
    os.makedirs("logs", exist_ok=True)

    # App 日誌
    app_logger = logging.getLogger("app")
    app_logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter("%(asctime)s - APP - %(levelname)s - %(message)s")
    ch0 = logging.StreamHandler()
    ch0.setFormatter(formatter)
    app_logger.addHandler(ch0)
    
    # Discord 日誌
    discord_logger = logging.getLogger("discord")
    discord_logger.setLevel(logging.INFO)
    formatter = logging.Formatter("%(asctime)s - Discord - %(levelname)s - %(message)s")
    
    ch = logging.StreamHandler()
    ch.setFormatter(formatter)
    discord_logger.addHandler(ch)
    
    fh1 = logging.FileHandler("logs/discord.log", encoding="utf-8")
    fh1.setFormatter(formatter)
    discord_logger.addHandler(fh1)
    
    # FastAPI/Uvicorn 日誌
    log_config = copy.deepcopy(LOGGING_CONFIG)
    log_config["formatters"]["default"]["fmt"] = "%(asctime)s - FastAPI - %(levelname)s - %(message)s"
    log_config["formatters"]["access"]["fmt"] = "%(asctime)s - FastAPI - %(levelname)s - %(client_addr)s - \"%(request_line)s\" %(status_code)s"
    log_config["handlers"]["file"] = {
        "formatter": "default",
        "class": "logging.FileHandler",
        "filename": "logs/app.log",
        "level": "INFO",
    }
    log_config["loggers"]["uvicorn.access"]["handlers"].append("file")
    log_config["loggers"]["uvicorn"]["handlers"].append("file")
    
    uvicorn_logger = logging.getLogger("uvicorn")
    uvicorn_logger.setLevel(logging.INFO)
    
    fh2 = logging.FileHandler("logs/app.log", encoding="utf-8")
    fh2.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
    uvicorn_logger.addHandler(fh2)
    
    return log_config

# ---------------- Discord Bot ----------------
intents = discord.Intents.all()
intents.message_content = True
bot = commands.Bot(command_prefix="?", intents=intents)

@bot.event
async def on_ready():
    discord_logger = logging.getLogger("discord")
    discord_logger.info(f"已登入 Discord：{bot.user}")

async def load_cogs():
    await bot.load_extension("cogs.general")
    await bot.add_cog(MusicCog(bot, playlist_manager))

# ---------------- FastAPI ----------------
app = FastAPI(
    title="Discord Music Bot API",
    description="Discord 音樂機器人的 Web API，提供播放控制、收藏管理等功能",
    version="1.0.0",
)
app.add_middleware(SessionMiddleware, secret_key=SESSION_SECRET)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- 全域錯誤處理 ----------------
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger = logging.getLogger("uvicorn")
    logger.error(f"Unhandled error: {exc}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Internal server error"},
    )

# ---------------- 路由 ----------------
app.include_router(auth_router, prefix="/auth", tags=["Auth"])
app.include_router(search_router, prefix="/search", tags=["Search"])
app.include_router(playlist_router, prefix="/playlist", tags=["Playlist"])
app.include_router(playback_router, prefix="/playback", tags=["Playback"])
app.include_router(favorites_router, prefix="/favorites", tags=["Favorites"])

@app.get("/health", tags=["Health"])
async def health_check():
    bot_ready = bot.is_ready()
    guild_count = len(bot.guilds) if bot_ready else 0
    return {
        "status": "ok",
        "bot_ready": bot_ready,
        "guild_count": guild_count,
        "active_playlists": len(playlist_manager.guild_playlists),
    }

app.state.bot = bot
app.state.playlist_manager = playlist_manager

# ---------------- 主執行 ----------------
async def main():
    await load_cogs()

    bot_task = asyncio.create_task(bot.start(DISCORD_TOKEN))

    log_config = setup_logging()
    api_config = uvicorn.Config(app, host=API_HOST, port=API_PORT, log_config=log_config)
    api_server = uvicorn.Server(api_config)
    api_task = asyncio.create_task(api_server.serve())

    await asyncio.gather(bot_task, api_task)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("程序中斷，正在退出...")
