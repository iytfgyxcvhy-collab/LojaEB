"""
Events cog for bot events.
"""

import discord
from discord.ext import commands
from bot.utils.logger import get_logger

logger = get_logger("events_cog")


class EventsCog(commands.Cog):
    """Cog for handling bot events."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        """Called when bot is ready."""
        logger.info(f"✅ Bot is ready! Logged in as {self.bot.user}")
        logger.info(f"✅ Serving {len(self.bot.guilds)} guild(s)")

        await self.bot.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.playing,
                name="LojaEB | /assinar para começar"
            )
        )

    @commands.Cog.listener()
    async def on_guild_join(self, guild: discord.Guild):
        """Called when bot joins a guild."""
        logger.info(f"✅ Joined guild: {guild.name} (ID: {guild.id})")

    @commands.Cog.listener()
    async def on_guild_remove(self, guild: discord.Guild):
        """Called when bot leaves a guild."""
        logger.info(f"❌ Removed from guild: {guild.name} (ID: {guild.id})")

    @commands.Cog.listener()
    async def on_app_command_error(
        self,
        interaction: discord.Interaction,
        error: discord.app_commands.AppCommandError
    ):
        """Handle app command errors."""
        logger.error(f"App command error: {str(error)}", exc_info=True)


async def setup(bot: commands.Bot) -> None:
    """Load events cog."""
    await bot.add_cog(EventsCog(bot))
