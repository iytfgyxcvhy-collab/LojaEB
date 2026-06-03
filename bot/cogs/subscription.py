"""
Subscription management cog.
"""

import discord
from discord.ext import commands
from discord import app_commands
from bot.services.subscription_service import SubscriptionService
from bot.utils import (
    get_logger,
    EmbedFactory,
    require_license,
    log_command,
    handle_errors
)
from datetime import datetime

logger = get_logger("subscription_cog")


class SubscriptionCog(commands.Cog):
    """Cog for subscription and license management."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.subscription_service = SubscriptionService()

    async def cog_load(self) -> None:
        """Initialize cog."""
        await self.subscription_service.initialize()
        logger.info("✅ SubscriptionCog loaded")

    @app_commands.command(name="assinar", description="Ver planos de assinatura e ativar licença")
    @log_command
    @handle_errors
    async def subscribe(self, interaction: discord.Interaction):
        """Subscription command showing available plans."""
        await interaction.response.defer(thinking=True)

        try:
            license_info = await self.subscription_service.get_license_info(interaction.guild_id)

            if license_info:
                status = "ativa" if license_info.get("status") == "active" else "inativa"
                expiration = license_info.get("expiration_date", datetime.utcnow())
                plan = license_info.get("plan", "Indefinido")
                
                embed = EmbedFactory.create_subscription_embed(
                    guild_name=interaction.guild.name,
                    status=status,
                    expiration_date=expiration.strftime("%d/%m/%Y %H:%M"),
                    plan=plan.capitalize()
                )
            else:
                embed = discord.Embed(
                    title="💎 Assinatura Premium",
                    description=f"**{interaction.guild.name}**\n\nEscolha um plano de assinatura:",
                    color=0xFFD700,
                    timestamp=datetime.now()
                )

                embed.add_field(
                    name="📅 Plano Diário",
                    value="🔹 1 dia de acesso\n🔹 R$ 9,99\n🔹 Perfeito para testar",
                    inline=False
                )

                embed.add_field(
                    name="📅 Plano Mensal",
                    value="🔹 30 dias de acesso\n🔹 R$ 29,99\n🔹 Mais popular",
                    inline=False
                )

                embed.add_field(
                    name="📅 Plano Trimestral",
                    value="🔹 90 dias de acesso\n🔹 R$ 79,99\n🔹 Melhor preço",
                    inline=False
                )

                embed.add_field(
                    name="✨ Benefícios",
                    value=(
                        "✅ Bot Ilimitado\n"
                        "✅ Todas as Funções Liberadas\n"
                        "✅ Dashboard Web\n"
                        "✅ Sistema de Loja\n"
                        "✅ Sistema de Tickets\n"
                        "✅ Backup Automático\n"
                        "✅ Atualizações Gratuitas\n"
                        "✅ Suporte Prioritário"
                    ),
                    inline=False
                )

                embed.set_footer(text="LojaEB | Gerenciador de Loja Discord")

            await interaction.followup.send(embed=embed)
            logger.info(f"Subscription info displayed for guild {interaction.guild_id}")

        except Exception as e:
            logger.error(f"Error in subscribe command: {str(e)}", exc_info=True)
            embed = EmbedFactory.create_error_embed(
                "Erro",
                "Ocorreu um erro ao processar sua solicitação."
            )
            await interaction.followup.send(embed=embed, ephemeral=True)

    @app_commands.command(name="status", description="Verificar status da licença do servidor")
    @log_command
    @handle_errors
    async def status(self, interaction: discord.Interaction):
        """Check license status for guild."""
        await interaction.response.defer(thinking=True)

        try:
            is_active = await self.subscription_service.check_license(interaction.guild_id)
            license_info = await self.subscription_service.get_license_info(interaction.guild_id)

            if is_active and license_info:
                days_left = await self.subscription_service.get_days_until_expiration(interaction.guild_id)
                embed = EmbedFactory.create_success_embed(
                    "Licença Ativa",
                    f"Sua licença está ativa e válida!\n\n"
                    f"**Plano:** {license_info.get('plan', 'Indefinido').capitalize()}\n"
                    f"**Dias Restantes:** {days_left or 'Indefinido'}\n"
                    f"**Expira em:** {license_info.get('expiration_date', 'Indefinido')}"
                )
            else:
                embed = EmbedFactory.create_license_expired_embed()

            await interaction.followup.send(embed=embed, ephemeral=True)
            logger.info(f"Status checked for guild {interaction.guild_id}")

        except Exception as e:
            logger.error(f"Error in status command: {str(e)}", exc_info=True)
            embed = EmbedFactory.create_error_embed(
                "Erro",
                "Ocorreu um erro ao verificar o status da licença."
            )
            await interaction.followup.send(embed=embed, ephemeral=True)


async def setup(bot: commands.Bot) -> None:
    """Load subscription cog."""
    await bot.add_cog(SubscriptionCog(bot))
