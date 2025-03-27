import discord
from discord.ext import commands
from discord import app_commands

from cogs import MusicCog
from utils.playlist import GuildPlaylistsManager
from dotenv import load_dotenv

import json
import os
import asyncio


intents = discord.Intents.all()  # 機器人的意圖 all/default/none
intents.message_content = True
bot = commands.Bot(command_prefix='?', intents=intents)
playlist_manager = GuildPlaylistsManager()


async def main():
  await bot.load_extension("cogs.general")
  await bot.add_cog(MusicCog(bot, playlist_manager))

load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

if __name__ == "__main__":
  asyncio.run(main())
  bot.run(DISCORD_TOKEN)
