from discord.ext import commands

class MainCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def search(ctx):
        await ctx.respond("Search")

def setup(bot):
    bot.add_cog(MainCommand(bot))