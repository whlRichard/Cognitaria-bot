import discord
import logging
import json
import aiofiles
from pathlib import Path

logger = logging.getLogger(__name__)

class RoleManager:
    def __init__(self, bot):
        self.bot = bot
        self.config_path = Path(__file__).parent.parent / 'data' / 'role_config.json'
        self.config = {}
        self._load_config()
        self.holographic_colors = [11127295, 16759788, 16761760]

    def _load_config(self):
        """Loads the role configuration from the JSON file."""
        try:
            self.config_path.parent.mkdir(exist_ok=True)
            if self.config_path.exists():
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if not content:
                        self.config = {}
                    else:
                        loaded_config = json.loads(content)
                        if isinstance(loaded_config, dict):
                            self.config = loaded_config
                        else:
                            logger.warning(f"配置文件根对象不是字典，已重置为空白配置: {self.config_path}")
                            self.config = {}
            else:
                self.config = {}
                with open(self.config_path, 'w', encoding='utf-8') as f:
                    json.dump({}, f)
                logger.info(f"配置文件不存在，已创建新的: {self.config_path}")
        except json.JSONDecodeError:
            logger.warning(f"配置文件损坏或为空: {self.config_path}。已重置为空白配置。")
            self.config = {}
        except Exception as e:
            logger.error(f"加载配置文件时发生错误: {e}", exc_info=True)
            self.config = {}

    async def _save_config(self):
        """Asynchronously saves the current role configuration to the JSON file."""
        try:
            async with aiofiles.open(self.config_path, 'w', encoding='utf-8') as f:
                await f.write(json.dumps(self.config, indent=4))
        except Exception as e:
            logger.error(f"保存配置文件时发生错误: {e}", exc_info=True)

    def _hex_to_color(self, hex_code):
        hex_code = hex_code.lstrip('#')
        if len(hex_code) != 6:
            raise ValueError("无效的十六进制颜色代码，必须是6位。")
        return discord.Color(int(hex_code, 16))

    def get_user_role_id(self, guild_id: int, user_id: int) -> int | None:
        """Gets the role ID for a user from the configuration."""
        return self.config.get(str(guild_id), {}).get(str(user_id))

    def get_user_role(self, guild: discord.Guild, user: discord.Member) -> discord.Role | None:
        """Gets the role for a user based on the stored ID."""
        role_id = self.get_user_role_id(guild.id, user.id)
        if role_id:
            return guild.get_role(role_id)
        return None

    async def create_or_update_role(self, guild: discord.Guild, user: discord.Member, colors_hex: list, role_name: str):
        """Creates or updates a user's color role and persists the ID."""
        role = self.get_user_role(guild, user)

        if len(colors_hex) >= 3:
            final_colors = [discord.Color(c) for c in self.holographic_colors]
            kwargs = {'name': role_name, 'colors': final_colors}
        elif len(colors_hex) == 2:
            final_colors = [self._hex_to_color(c) for c in colors_hex]
            kwargs = {'name': role_name, 'colors': final_colors}
        elif len(colors_hex) == 1:
            final_color = self._hex_to_color(colors_hex[0])
            kwargs = {'name': role_name, 'color': final_color}
        else:
            raise ValueError("必须提供至少一种颜色。")

        target_role = role
        if role:
            logger.info(f"正在为用户 {user.id} 更新角色 {role.id}...")
            # 更新现有角色时，可以附带位置信息
            try:
                target_position = user.top_role.position + 1
                bot_max_position = guild.me.top_role.position
                if target_position >= bot_max_position:
                    target_position = bot_max_position - 1
                kwargs['position'] = target_position
            except AttributeError:
                logger.warning("无法确定用户或机器人的最高角色，将使用默认位置。")
            
            await role.edit(**kwargs)
        else:
            logger.info(f"正在为用户 {user.id} 创建新角色...")
            # 创建角色时，不能直接指定位置
            new_role = await guild.create_role(**kwargs)
            
            # 创建后，再单独编辑其位置
            try:
                target_position = user.top_role.position + 1
                bot_max_position = guild.me.top_role.position
                if target_position >= bot_max_position:
                    target_position = bot_max_position - 1
                await new_role.edit(position=target_position)
                logger.info(f"已将角色 {new_role.name} 的位置调整到 {target_position}")
            except AttributeError:
                 logger.warning("无法确定用户或机器人的最高角色，将使用默认位置。")
            except Exception as e:
                logger.error(f"调整角色位置时出错: {e}", exc_info=True)

            await user.add_roles(new_role)
            target_role = new_role
        
        if target_role:
            guild_id_str = str(guild.id)
            user_id_str = str(user.id)
            if guild_id_str not in self.config:
                self.config[guild_id_str] = {}
            self.config[guild_id_str][user_id_str] = target_role.id
            await self._save_config()

        logger.info(f"为用户 {user.id} 的操作已成功完成。")

    async def remove_role(self, guild: discord.Guild, user: discord.Member):
        """Removes a user's color role and updates the configuration."""
        role = self.get_user_role(guild, user)
        if role:
            logger.info(f"正在为用户 {user.id} 删除角色 {role.id}...")
            role_id_to_remove = role.id
            await role.delete(reason="用户请求移除颜色身份组")
            
            guild_id_str = str(guild.id)
            user_id_str = str(user.id)
            if guild_id_str in self.config and user_id_str in self.config[guild_id_str]:
                if self.config[guild_id_str][user_id_str] == role_id_to_remove:
                    del self.config[guild_id_str][user_id_str]
                    if not self.config[guild_id_str]:
                        del self.config[guild_id_str]
                    await self._save_config()
            return True
        return False