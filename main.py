import discord
from discord.ext import commands
from discord import app_commands
from music import GuildPlaylistsManager, Music_bot
from dotenv import load_dotenv

import json
import os
import asyncio

intents = discord.Intents.all()  #機器人的意圖 all/default/none
intents.message_content = True
bot = commands.Bot(command_prefix='?', intents=intents)
playlist_manager = GuildPlaylistsManager()

async def sync_commands():
  try:
    synced = await bot.tree.sync()
    print(f'Synced {len(synced)} Commands')
  except Exception as e:
    print(e)


@bot.event
async def on_ready():
  game = discord.Game("Playing a game", type=1) 
  await bot.change_presence(status=discord.Status.online, activity=game)
  print('BOT is online')
  await sync_commands()

@bot.command()
async def reload_music(ctx):
  await bot.remove_cog('Music_bot')
  await load_music()
  await ctx.send(f'Re-Loaded player done.')
  await sync_commands()
  
async def load_music():
  await bot.add_cog(Music_bot(bot, playlist_manager))

async def main():
  await load_music()

load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

if __name__ == "__main__":
  asyncio.run(main())
  bot.run(DISCORD_TOKEN)
