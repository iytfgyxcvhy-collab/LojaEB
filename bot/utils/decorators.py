"""
Decorators for bot commands and functions.
"""

import functools
import discord
from discord.ext import commands
from bot.utils.logger import get_logger
from bot.utils.embeds import EmbedFactory

logger = get_logger("decorators")


def require_license(func):
    """Decorator to check if guild has active license."""
    @functools.wraps(func)
    async def wrapper(self, interaction: discord.Interaction, *args, **kwargs):
        from bot.services.subscription_service import SubscriptionService

        service = SubscriptionService()
        await service.initialize()
        is_active = await service.check_license(interaction.guild_id)

        if not is_active:
            embed = EmbedFactory.create_license_expired_embed()
            await interaction.response.send_message(embed=embed, ephemeral=True)
            logger.warning(f"Blocked command for guild {interaction.guild_id} - No active license")
            return

        return await func(self, interaction, *args, **kwargs)

    return wrapper


def require_admin(func):
    """Decorator to check if user is admin."""
    @functools.wraps(func)
    async def wrapper(self, interaction: discord.Interaction, *args, **kwargs):
        if not interaction.user.guild_permissions.administrator:
            embed = EmbedFactory.create_error_embed(
                "Permissão Negada",
                "Apenas administradores podem executar este comando."
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
            logger.warning(f"Admin command blocked for user {interaction.user.id}")
            return

        return await func(self, interaction, *args, **kwargs)

    return wrapper


def log_command(func):
    """Decorator to log command execution."""
    @functools.wraps(func)
    async def wrapper(self, interaction: discord.Interaction, *args, **kwargs):
        logger.info(
            f"Command executed: {func.__name__} | "
            f"User: {interaction.user.id} | "
            f"Guild: {interaction.guild_id}"
        )
        return await func(self, interaction, *args, **kwargs)

    return wrapper


def handle_errors(func):
    """Decorator to handle errors globally."""
    @functools.wraps(func)
    async def wrapper(self, interaction: discord.Interaction, *args, **kwargs):
        try:
            return await func(self, interaction, *args, **kwargs)
        except Exception as e:
            logger.error(f"Error in {func.__name__}: {str(e)}", exc_info=True)
            embed = EmbedFactory.create_error_embed(
                "Erro Inesperado",
                f"Ocorreu um erro ao executar o comando.\n\n`{str(e)}`"
            )
            try:
                await interaction.response.send_message(embed=embed, ephemeral=True)
            except:
                pass
            return

    return wrapper
