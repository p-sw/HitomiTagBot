import discord
from discord.commands import SlashCommandGroup
import requests
from db import DB_OBJECT

class Commands(discord.Cog):
    def __init__(self, bot: discord.Bot):
        self.bot = bot
    
    bookmark = SlashCommandGroup("bookmark", "북마크에 관한 명령어입니다.")
    
    manage = bookmark.create_subgroup("manage", "북마크를 관리합니다.")
    # online = bookmark.create_subgroup("online", "온라인 북마크에 관한 명령어입니다.")

    async def script_strdata(self, product, key):
        res = requests.get(f'https://ltn.hitomi.la/galleries/{product}.js')
        start_index = res.text.find(f'"{key}"')+len(key)+4
        end_index = res.text.find('"', start_index+1)
        return res.text[start_index:end_index]

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
        ),
        searches: discord.Option(
            str,
            "검색어를 설정합니다. 이후 북마크를 검색할 때 입력합니다.\n공백으로 구분됩니다. (최소 1개)"
        )
    ):
        found = DB_OBJECT.execute_result(f"SELECT uid FROM Bookmarks WHERE product_id='{product}'")
        if found:
            if str(ctx.author.id) in [item[0] for item in found]:
                await ctx.respond('이미 추가된 북마크입니다.\n정보를 수정하려면 `/bookmark manage edit`를 사용해주세요.')
                return
        title_data = await self.script_strdata(product, "title")
        DB_OBJECT.execute(f"INSERT INTO Bookmarks VALUES ('{ctx.author.id}', '{product}', '{title_data}', '{searches}')")
        DB_OBJECT.commit()
        await ctx.respond('북마크가 성공적으로 추가되었습니다.')
    
    @manage.command(
        name="edit",
        description="북마크 정보를 수정합니다."
    )
    async def edit_bookmark(
        self,
        ctx,
        what: discord.Option(
            str,
            "어떤 정보를 수정할지 결정합니다.",
            choices=[
                discord.OptionChoice(
                    name="품번",
                    value="product_id"
                ),
                discord.OptionChoice(
                    name="검색어",
                    value="search"
                )
            ]
        ),
        from_id: discord.Option(
            str,
            "수정 이전의 품번을 적어주세요."
        ),
        to: discord.Option(
            str,
            "수정할 정보를 적어주세요."
        )
    ):
        found = DB_OBJECT.execute_result(f"SELECT uid FROM Bookmarks WHERE product_ids='{from_id}'")
        if not found or str(ctx.author.id) not in [item[0] for item in found]:
            await ctx.respond('북마크를 찾지 못했습니다.\n먼저 `/bookmark manage add`를 이용해 등록해주세요.')
            return
        sql = f"UPDATE Bookmarks SET {what}='{to}' WHERE product_id='{from_id}'"
        DB_OBJECT.execute(sql)
        DB_OBJECT.commit()
        await ctx.respond('북마크를 성공적으로 수정했습니다.')
    
    @manage.command(
        name="delete",
        description="북마크를 삭제합니다."
    )
    async def delete_bookmark(
        self,
        ctx,
        product: discord.Option(
            str,
            "품번을 여기에 입력합니다."
        )
    ):
        found = DB_OBJECT.execute_result(f"SELECT uid FROM Bookmarks WHERE product_id='{product}'")
        if not found or str(ctx.author.id) not in [item[0] for item in found]:
            await ctx.respond('북마크를 찾을 수 없습니다.')
            return
        DB_OBJECT.execute(f"DELETE FROM Bookmarks WHERE uid='{ctx.author.id}' AND product_id='{product}'")
        DB_OBJECT.commit()
        await ctx.respond('북마크를 성공적으로 제거했습니다.')
    
    @bookmark.command(
        name="search",
        description="자신의 북마크를 검색합니다."
    )
    async def search_mine(
        self, 
        ctx,
        search_tag: discord.Option(
            str,
            "검색어를 이용해 자신의 북마크를 검색합니다.\n공백으로 다중 검색을 이용할 수 있습니다."
        ),
        page: discord.Option(
            int,
            "여기에 페이지 수를 입력해 검색 결과가 10개 이상일 경우 쉽게 찾아보세요."
        ) = 1
    ):
        SEARCH_LIMIT = 10
        search_tags = search_tag.split()
        sql = "SELECT product_id, title FROM Bookmarks WHERE uid='{}' AND ({})"
        query_str = []
        for search in search_tags:
            query_str.append("(search LIKE '{0} %' or search LIKE '% {0} %' or search LIKE '% {0}')".format(search))
        result = DB_OBJECT.execute_result(sql.format(str(ctx.author.id), ' AND '.join(query_str)))
        embed = discord.Embed(
            title="검색 결과",
            description=f"총 **{len(result)}**건의 결과\n",
            color=0x32ff32
        )
        result_txt_format = "{1}: [{0}](https://hitomi.la/galleries/{1}.html)"
        if len(result) > 10:
            page_start = (page - 1) * SEARCH_LIMIT
            page_end = page * SEARCH_LIMIT
            result = result[page_start:page_end]
        no_msg = "검색된 북마크가 없습니다."
        embed.add_field(
            name="***",
            value="\n\n".join([result_txt_format.format(item[1], item[0]) for item in result]) if result else no_msg
        )
        await ctx.respond(embed=embed)


def setup(bot):
    bot.add_cog(Commands(bot))