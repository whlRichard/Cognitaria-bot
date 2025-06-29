import discord
import logging
import random

logger = logging.getLogger(__name__)

class RoleSettingsModal(discord.ui.Modal):
    def __init__(self, is_update=False, current_name=None, current_colors=None, original_message: discord.Message = None):
        super().__init__(title="创建/修改你的专属身份组")
        self.is_update = is_update
        self.original_message = original_message
        colors_str = ", ".join(current_colors) if current_colors else ""

        self.role_name = discord.ui.InputText(label="身份组名字", value=current_name or "", required=True)
        self.primary_color = discord.ui.InputText(label="身份组颜色 (HEX, e.g., #RRGGBB)", value=colors_str, required=True)
        self.secondary_color = discord.ui.InputText(label="第二个颜色 (可选)", placeholder="e.g., #RRGGBB", required=False)
        self.tertiary_color = discord.ui.InputText(label="第三个颜色 (可选)", placeholder="e.g., #RRGGBB", required=False)
        
        self.add_item(self.role_name)
        self.add_item(self.primary_color)
        self.add_item(self.secondary_color)
        self.add_item(self.tertiary_color)

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.defer()
        status_message = ""
        try:
            role_manager = interaction.client.role_manager
            role_name = self.role_name.value
            
            # 检查是否输入了第三种颜色
            if self.tertiary_color.value:
                # 如果是，则强制使用全息颜色
                colors_hex = [
                    f"#{11127295:06x}",
                    f"#{16759788:06x}",
                    f"#{16761760:06x}"
                ]
            else:
                # 否则，使用用户输入的颜色
                colors_hex = [self.primary_color.value.strip()]
                if self.secondary_color.value:
                    colors_hex.append(self.secondary_color.value.strip())
            
            # 去重
            colors_hex = list(dict.fromkeys(colors_hex))
            
            await role_manager.create_or_update_role(
                guild=interaction.guild,
                user=interaction.user,
                colors_hex=colors_hex,
                role_name=role_name
            )
            status_message = f"\n\n**✅ 操作成功:** 身份组 `{role_name}` 已成功保存！"
        except ValueError as e:
            status_message = f"\n\n**❌ 操作失败:** {e}"
        except Exception as e:
            logger.error(f"创建或更新角色时发生未知错误: {e}", exc_info=True)
            status_message = "\n\n**❌ 操作失败:** 发生了一个意料之外的错误，请联系管理员。"

        # --- Edit the original message ---
        if self.original_message:
            original_embed = self.original_message.embeds[0]
            new_description = original_embed.description.split("\n\n**")[0] + status_message
            new_embed = discord.Embed(
                title=original_embed.title,
                description=new_description,
                color=discord.Color.random()
            )
            await interaction.followup.edit_message(self.original_message.id, embed=new_embed)


class ColorSelectionView(discord.ui.View):
   def __init__(self):
       super().__init__(timeout=900)

   @discord.ui.button(label="创建 / 更改颜色", style=discord.ButtonStyle.primary, custom_id="persistent_color_view:upsert")
   async def upsert_color(self, button: discord.ui.Button, interaction: discord.Interaction):
       logger.info(f"Button 'upsert_color' clicked by {interaction.user.id}")
       role_manager = interaction.client.role_manager
       user_role = role_manager.get_user_role(interaction.guild, interaction.user)
       
       is_update = user_role is not None
       current_name, current_colors = None, None
       if is_update:
           current_name = user_role.name
           if user_role.color.value != 0:
               current_colors = [f"#{user_role.color.value:06x}"]

       modal = RoleSettingsModal(is_update, current_name, current_colors, original_message=interaction.message)
       await interaction.response.send_modal(modal)


   @discord.ui.button(label="移除颜色", style=discord.ButtonStyle.danger, custom_id="persistent_color_view:remove")
   async def remove_color(self, button: discord.ui.Button, interaction: discord.Interaction):
       logger.info(f"Button 'remove_color' clicked by {interaction.user.id}")
       role_manager = interaction.client.role_manager
       status_message = ""
       
       try:
           was_removed = await role_manager.remove_role(interaction.guild, interaction.user)
           if was_removed:
               status_message = "\n\n**✅ 操作成功:** 你的专属颜色身份组已成功移除。"
           else:
               status_message = "\n\n**ℹ️ 提示:** 你还没有创建专属颜色身份组，无需移除。"
       except Exception as e:
           logger.error(f"移除角色时发生未知错误: {e}", exc_info=True)
           status_message = "\n\n**❌ 操作失败:** 发生了一个意料之外的错误，请联系管理员。"

       # --- Edit the original message ---
       original_embed = interaction.message.embeds[0]
       new_description = original_embed.description.split("\n\n**")[0] + status_message
       new_embed = discord.Embed(
           title=original_embed.title,
           description=new_description,
           color=discord.Color.random()
       )
       await interaction.response.edit_message(embed=new_embed)
