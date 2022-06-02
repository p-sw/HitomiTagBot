from settings import apps, tester_ids
import discord

bot = discord.Bot(debug_guilds=tester_ids)

#* Bot code *#
@bot.event
async def on_ready():
    print(f"Started bot as {bot.user}")

for app in apps:
    bot.load_extension(app)
