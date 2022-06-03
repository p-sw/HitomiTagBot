from settings import apps, tester_ids
import discord

bot = discord.Bot(debug_guilds=tester_ids)

for app in apps:
    print(f"Loading Cog: {app}")
    bot.load_extension(app)
    print(f"Cog loaded..")
print(f"Bot fully loaded.")