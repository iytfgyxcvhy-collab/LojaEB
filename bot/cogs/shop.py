"""
Shop management cog.
"""

import discord
from discord.ext import commands
from discord import app_commands
from bot.services.shop_service import ShopService
from bot.utils import (
    get_logger,
    EmbedFactory,
    require_license,
    require_admin,
    log_command,
    handle_errors
)

logger = get_logger("shop_cog")


class ShopCog(commands.Cog):
    """Cog for shop management."""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.shop_service = ShopService()

    async def cog_load(self) -> None:
        """Initialize cog."""
        await self.shop_service.initialize()
        logger.info("✅ ShopCog loaded")

    @app_commands.command(name="catalogo", description="Ver catálogo de produtos da loja")
    @require_license
    @log_command
    @handle_errors
    async def catalog(self, interaction: discord.Interaction):
        """Display product catalog."""
        await interaction.response.defer(thinking=True)

        try:
            products = await self.shop_service.get_products_by_guild(interaction.guild_id)

            if not products:
                embed = EmbedFactory.create_warning_embed(
                    "Catálogo Vazio",
                    "Nenhum produto disponível no momento."
                )
                await interaction.followup.send(embed=embed, ephemeral=True)
                return

            embed = discord.Embed(
                title="🛍️ Catálogo de Produtos",
                description=f"Total de {len(products)} produto(s) disponível(is)",
                color=0x7289DA
            )

            for product in products[:10]:
                embed.add_field(
                    name=f"📦 {product.get('name')}",
                    value=(
                        f"💰 **Preço:** R$ {product.get('price', 0):.2f}\n"
                        f"📊 **Estoque:** {product.get('stock', 0)} un.\n"
                        f"📝 {product.get('description', 'Sem descrição')[:100]}..."
                    ),
                    inline=False
                )

            embed.set_footer(text="LojaEB | Gerenciador de Loja Discord")
            await interaction.followup.send(embed=embed)
            logger.info(f"Catalog displayed for guild {interaction.guild_id}")

        except Exception as e:
            logger.error(f"Error in catalog command: {str(e)}", exc_info=True)
            embed = EmbedFactory.create_error_embed(
                "Erro",
                "Ocorreu um erro ao exibir o catálogo."
            )
            await interaction.followup.send(embed=embed, ephemeral=True)

    @app_commands.command(name="categorias", description="Ver categorias de produtos")
    @require_license
    @log_command
    @handle_errors
    async def categories(self, interaction: discord.Interaction):
        """Display product categories."""
        await interaction.response.defer(thinking=True)

        try:
            categories = await self.shop_service.get_categories(interaction.guild_id)

            if not categories:
                embed = EmbedFactory.create_warning_embed(
                    "Sem Categorias",
                    "Nenhuma categoria criada ainda."
                )
                await interaction.followup.send(embed=embed, ephemeral=True)
                return

            embed = discord.Embed(
                title="📂 Categorias de Produtos",
                description=f"Total de {len(categories)} categoria(s)",
                color=0x7289DA
            )

            for category in categories:
                embed.add_field(
                    name=f"{category.get('emoji')} {category.get('name')}",
                    value=category.get('description', 'Sem descrição'),
                    inline=False
                )

            embed.set_footer(text="LojaEB | Gerenciador de Loja Discord")
            await interaction.followup.send(embed=embed)
            logger.info(f"Categories displayed for guild {interaction.guild_id}")

        except Exception as e:
            logger.error(f"Error in categories command: {str(e)}", exc_info=True)
            embed = EmbedFactory.create_error_embed(
                "Erro",
                "Ocorreu um erro ao exibir as categorias."
            )
            await interaction.followup.send(embed=embed, ephemeral=True)


async def setup(bot: commands.Bot) -> None:
    """Load shop cog."""
    await bot.add_cog(ShopCog(bot))
