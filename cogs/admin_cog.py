import discord
from discord.ext import commands
from discord.commands import SlashCommandGroup

class AdminCog(commands.Cog):
    """Admin commands for bot management."""
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    admin = SlashCommandGroup("admin", "Admin commands for bot management")

    @admin.command(name="reload", description="Reloads a specified cog or all cogs.")
    @commands.is_owner()
    async def reload(self, ctx: discord.ApplicationContext, cog_name: str = None):
        """Reloads a cog or all cogs."""
        if cog_name:
            try:
                self.bot.reload_extension(cog_name)
                await ctx.respond(f"✅ Cog `{cog_name}` has been reloaded.", ephemeral=True)
            except Exception as e:
                await ctx.respond(f"❌ Failed to reload cog `{cog_name}`: {e}", ephemeral=True)
        else:
            reloaded_cogs = []
            failed_cogs = []
            for extension in list(self.bot.extensions.keys()):
                try:
                    self.bot.reload_extension(extension)
                    reloaded_cogs.append(f"`{extension}`")
                except Exception as e:
                    failed_cogs.append(f"`{extension}` ({e})")
            
            response = ""
            if reloaded_cogs:
                response += f"✅ Reloaded cogs: {', '.join(reloaded_cogs)}\n"
            if failed_cogs:
                response += f"❌ Failed to reload cogs: {', '.join(failed_cogs)}"
            
            await ctx.respond(response.strip(), ephemeral=True)

    @admin.command(name="sync", description="Syncs application commands with Discord.")
    @commands.is_owner()
    async def sync(self, ctx: discord.ApplicationContext):
        """Syncs commands."""
        await ctx.defer(ephemeral=True)
        try:
            await self.bot.sync_commands()
            await ctx.followup.send("✅ Commands have been synced globally.")
        except Exception as e:
            await ctx.followup.send(f"❌ Failed to sync commands: {e}")

def setup(bot: commands.Bot):
    bot.add_cog(AdminCog(bot))