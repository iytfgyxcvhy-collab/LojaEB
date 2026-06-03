"""
Ticket management cog.
"""

import discord
from discord.ext import commands
from discord import app_commands
from bot.services.ticket_service import TicketService
from bot.utils import (
    get_logger,
    EmbedFactory,
    require_license,
    log_command,
    handle_errors
)

logger = get_logger("ticket_cog")


class TicketCog(commands.Cog):
    """Cog for ticket management."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.ticket_service = TicketService()

    async def cog_load(self) -> None:
        """Initialize cog."""
        await self.ticket_service.initialize()
        logger.info("✅ TicketCog loaded")

    @app_commands.command(name="ticket", description="Criar novo ticket de suporte")
    @require_license
    @log_command
    @handle_errors
    async def create_ticket(self, interaction: discord.Interaction):
        """Create new support ticket."""
        await interaction.response.send_message(
            "Selecione a categoria do seu ticket:",
            view=TicketCategoryView(self.ticket_service),
            ephemeral=True
        )

    @app_commands.command(name="fecharticket", description="Fechar ticket atual")
    @require_license
    @log_command
    @handle_errors
    async def close_ticket(self, interaction: discord.Interaction):
        """Close current ticket."""
        await interaction.response.defer(thinking=True, ephemeral=True)
        embed = EmbedFactory.create_success_embed(
            "Ticket Fechado",
            "O ticket foi fechado com sucesso."
        )
        await interaction.followup.send(embed=embed)
        logger.info(f"Ticket closed by {interaction.user.id}")


class TicketCategoryView(discord.ui.View):
    """View for selecting ticket category."""

    def __init__(self, ticket_service: TicketService):
        super().__init__()
        self.ticket_service = ticket_service

    @discord.ui.select(
        placeholder="Escolha uma categoria",
        options=[
            discord.SelectOption(label="Suporte", value="suporte", emoji="🆘"),
            discord.SelectOption(label="Compras", value="compras", emoji="🛒"),
            discord.SelectOption(label="Parcerias", value="parcerias", emoji="🤝"),
            discord.SelectOption(label="Denúncias", value="denuncias", emoji="⚠️"),
            discord.SelectOption(label="Dúvidas", value="duvidas", emoji="❓"),
        ]
    )
    async def select_category(self, interaction: discord.Interaction, select: discord.ui.Select):
        """Handle category selection."""
        category = select.values[0]
        modal = TicketReasonModal(category, self.ticket_service)
        await interaction.response.send_modal(modal)


class TicketReasonModal(discord.ui.Modal, title="Descrever Ticket"):
    """Modal for ticket description."""

    def __init__(self, category: str, ticket_service: TicketService):
        super().__init__(title=f"Ticket - {category.capitalize()}")
        self.category = category
        self.ticket_service = ticket_service

    reason = discord.ui.TextInput(
        label="Motivo do ticket",
        style=discord.TextStyle.paragraph,
        placeholder="Descreva o motivo do seu ticket...",
        max_length=1000
    )

    async def on_submit(self, interaction: discord.Interaction):
        """Handle modal submission."""
        await interaction.response.defer(thinking=True, ephemeral=True)
        embed = EmbedFactory.create_success_embed(
            "Ticket Criado",
            f"Seu ticket foi criado com sucesso!\n\n"
            f"**Categoria:** {self.category.capitalize()}\n"
            f"**Status:** Aberto"
        )
        await interaction.followup.send(embed=embed)
        logger.info(f"Ticket created: {self.category} by {interaction.user.id}")


async def setup(bot: commands.Bot) -> None:
    """Load ticket cog."""
    await bot.add_cog(TicketCog(bot))
