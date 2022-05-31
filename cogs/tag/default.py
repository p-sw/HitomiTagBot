import discord
from discord.ext import commands
from settings import tester_ids

class MainCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.slash_command(guild_ids=tester_ids)
    async def test_sum(
        self,
        ctx, 
        first: discord.Option(int), 
        second: discord.Option(int)
    ):
        await ctx.respond(str(first+second))

def setup(bot):
    bot.add_cog(MainCommand(bot))