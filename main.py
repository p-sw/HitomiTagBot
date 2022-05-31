from settings import apps
import discord

bot = discord.Bot()

#* Bot code *#
@bot.event
async def on_ready():
    print(f"Started bot as {bot.user}")

for app in apps:
    bot.load_extension(app)
