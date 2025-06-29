import discord
from discord.ext import commands
import os
import logging
from pathlib import Path
from dotenv import load_dotenv
from core.role_manager import RoleManager
from cogs.color_cog.ui import ColorSelectionView

# --- 类型提示 ---
# 这是关键修改：让 IDE 知道 bot.role_manager 的类型
class CognitariaBot(commands.Bot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.role_manager: RoleManager = None

# --- 日志记录设置 ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# --- 加载环境变量 ---
dotenv_path = Path(__file__).parent / '.env'
load_dotenv(dotenv_path=dotenv_path)
TOKEN = os.getenv("DISCORD_TOKEN")
if not TOKEN:
    raise ValueError(f"在路径 {dotenv_path} 中未找到或未正确配置 DISCORD_TOKEN")

# --- Bot 实例 ---
bot = CognitariaBot()

# --- 启动前的设置钩子 ---
@bot.event
async def on_ready():
    logger.info(f'机器人 {bot.user} 已成功登录并准备就绪!')

# --- 加载 Cogs ---
def load_cogs(bot_instance: CognitariaBot):
    bot_instance.role_manager = RoleManager(bot_instance)
    cogs_to_load = ['cogs.admin_cog', 'cogs.color_cog.cog']
    for cog in cogs_to_load:
        try:
            bot_instance.load_extension(cog)
            logger.info(f"成功加载 Cog: {cog}")
        except Exception as e:
            logger.error(f"加载 Cog {cog} 失败: {e}", exc_info=True)

# --- 运行 Bot ---
if __name__ == "__main__":
    load_cogs(bot)
    bot.run(TOKEN)