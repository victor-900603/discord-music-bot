import discord
from discord.ext import commands
import logging

logger = logging.getLogger("discord")

class BotEvents(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def sync_commands(self):
        try:
            synced = await self.bot.tree.sync()
            logger.info(f'Synced {len(synced)} Commands')
        except Exception as e:
            logger.error("Failed to sync commands", exc_info=e)

    @commands.Cog.listener()
    async def on_ready(self):
        # game = discord.Game("哈哈是我啦")
        activity = discord.Activity(type=discord.ActivityType.listening, name="🎵 五月天 🎵")
        await self.bot.change_presence(status=discord.Status.online, activity=activity)
        print('BOT is online')
        await self.sync_commands()
        
    @commands.command()
    async def latency(self, ctx):
        latency = round(self.bot.latency * 1000, 2)
        await ctx.send(f'Latency: {latency}ms')

async def setup(bot):
    await bot.add_cog(BotEvents(bot))
