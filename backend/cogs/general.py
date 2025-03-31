import discord
from discord.ext import commands

class BotEvents(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def sync_commands(self):
        try:
            synced = await self.bot.tree.sync()
            print(f'Synced {len(synced)} Commands')
        except Exception as e:
            print(e)

    @commands.Cog.listener()
    async def on_ready(self):
        game = discord.Game("我", type=1)
        await self.bot.change_presence(status=discord.Status.online, activity=game)
        print('BOT is online')
        await self.sync_commands()
        
    @commands.command()
    async def latency(self, ctx):
        latency = round(self.bot.latency * 1000, 2)
        await ctx.send(f'Latency: {latency}ms')

    # @commands.command()
    # async def reload_music(self, ctx):
    #     await self.bot.remove_cog('MusicCog')
    #     await load_music()
    #     await ctx.send('Re-Loaded player done.')
    #     await self.sync_commands()

async def setup(bot):
    await bot.add_cog(BotEvents(bot))
