import discord
from discord.ext import commands
from settings import tester_ids
from db import DB_OBJECT

class MainCommand(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.slash_command(
        name="search", 
        description="태그 검색",
        guild_ids=tester_ids
    )
    async def search(
        self,
        ctx, 
        prefix: discord.Option(
            str,
            "태그의 종류를 나타냅니다.",
            choices=[
                discord.OptionChoice(
                    name="female(여성)",
                    value="female"
                ),
                discord.OptionChoice(
                    name="male(남성)",
                    value="male"
                ),
                discord.OptionChoice(
                    name="type(공통)",
                    value="type"
                )
            ]
        ), 
        name: discord.Option(str, "태그를 입력해주세요.\n(띄어쓰기는 _로 처리)")
    ):
        embed = discord.Embed(title="검색 결과")
        query = f"SELECT * FROM Tags WHERE prefix='{prefix}' AND tag='{name}'"
        query_result = DB_OBJECT.execute_result(query)
        if not query_result:
            embed.description = "태그가 존재하지 않습니다.\n철자를 확인하고 다시 시도해주세요."
            embed.color = 0xff3232
        else:
            default_data = '정보가 등록되지 않았습니다.'
            data = query_result[0]
            embed.add_field(
                name='태그',
                value=f'{data[0]}:{data[1]}',
                inline=False
            )
            embed.add_field(
                name="작품 개수",
                value=f'{data[2]} 개',
                inline=True
            )
            korean_tag = f'{data[0]}:{data[3]}' if data[3] else default_data
            korean_desc = data[4] if data[4] else default_data
            embed.add_field(
                name="한국어 정보",
                value=f'태그 번역: {korean_tag}\n태그 설명: {korean_desc}',
                inline=False
            )
            embed.color = 0x32FF32
        await ctx.respond(embed=embed)

def setup(bot):
    bot.add_cog(MainCommand(bot))