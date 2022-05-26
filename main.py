from settings import *
import discord

bot = discord.Bot()

#* Utils *#
class command_wrapper(object):
    def __init__(self, **kwargs):
        self.args = kwargs
    def __call__(self, func):
        def wrapper():
            if ENV_NAME == "STAGE":
                self.args['guild_ids'] = command_guild_id
                return func(**self.args)
            elif ENV_NAME == "PRODUCT":
                return func(**self.args)

#* Bot code *#
@bot.event
async def on_ready():
    print(f"Started bot as {bot.user}")

@command_wrapper()
@bot.slash_command()
async def hello(ctx):
    await ctx.respond("Hello!")

bot.run(bot_token)