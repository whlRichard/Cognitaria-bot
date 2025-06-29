import discord
import random
from discord.ext import commands
from .ui import ColorSelectionView

class ColorCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(name="color_panel", description="显示颜色管理面板。")
    async def color_panel(self, ctx: discord.ApplicationContext):
        embed = discord.Embed(
            title="🎨 颜色身份组管理",
            description="在这里，你可以创建、修改或移除你的专属颜色身份组。\n\n**如何使用**:\n- **创建/修改**: 点击按钮，在弹窗中设置你的身份组名称和颜色。\n- **移除**: 如果你已有身份组，点击按钮即可移除。\n\n**颜色代码**: 请使用标准的十六进制颜色代码 (例如: `#FF00FF`)。",
            color=discord.Color.random()
        )
        # 关键修复：调用时不传递任何参数，与 bot.py 中的 add_view 一致
        await ctx.respond(embed=embed, view=ColorSelectionView(), ephemeral=True)

def setup(bot):
    bot.add_cog(ColorCog(bot))