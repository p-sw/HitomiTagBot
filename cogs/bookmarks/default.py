import discord
from discord.commands import SlashCommandGroup

class Commands(discord.Cog):
    def __init__(self, bot: discord.Bot):
        self.bot = bot
    
    bookmark = SlashCommandGroup("bookmark", "북마크에 관한 명령어입니다.")
    
    manage = bookmark.create_subgroup("manage", "북마크를 관리합니다.")
    online = bookmark.create_subgroup("online", "온라인 북마크에 관한 명령어입니다.")

    @manage.command(
        name="add",
        description="북마크를 추가합니다."
    )
    async def add_bookmark(
        self, 
        ctx, 
        product: discord.Option(
            str,
            "품번을 여기에 입력합니다. 뷰어로 들어간 후 고유번호를 확인 할 수 있습니다.\n(https://hitomi.la/viewer/여기가_품번.html)"
        )):
        await ctx.respond('개발중입니다.')


def setup(bot):
    bot.add_cog(Commands(bot))