import discord
from discord.ext import commands

class BaseEventHandler(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_ready(self):
        print(f"Logged in as {self.bot.user}")

class BaseCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

def setup(bot):
    bot.add_cog(BaseEventHandler(bot))
    bot.add_cog(BaseCommand(bot))