"""
Embeds factory for consistent Discord embeds across the bot.
"""

import discord
from datetime import datetime
from enum import Enum


class EmbedColor(Enum):
    """Standard embed colors."""
    PRIMARY = 0x7289DA  # Discord blue
    SUCCESS = 0x43B581  # Green
    WARNING = 0xFAA61A  # Orange
    DANGER = 0xF04747   # Red
    INFO = 0x00B0F4    # Light blue
    PREMIUM = 0xFFD700  # Gold


class EmbedFactory:
    """Factory for creating consistent embeds."""

    @staticmethod
    def create_subscription_embed(
        guild_name: str,
        status: str,
        expiration_date: str,
        plan: str = "Indefinido"
    ) -> discord.Embed:
        """Create subscription status embed."""
        embed = discord.Embed(
            title="💎 Assinatura Premium",
            description=f"**{guild_name}**",
            color=EmbedColor.PREMIUM.value,
            timestamp=datetime.now()
        )

        status_emoji = "✅" if status == "ativa" else "❌"
        embed.add_field(
            name="Status Atual",
            value=f"{status_emoji} {status.capitalize()}",
            inline=False
        )

        embed.add_field(
            name="Plano Ativo",
            value=plan,
            inline=False
        )

        embed.add_field(
            name="Expira em",
            value=expiration_date,
            inline=False
        )

        embed.add_field(
            name="Benefícios",
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
        return embed

    @staticmethod
    def create_license_expired_embed() -> discord.Embed:
        """Create license expired embed."""
        embed = discord.Embed(
            title="🔒 Licença Expirada",
            description="Este servidor não possui uma assinatura ativa.",
            color=EmbedColor.DANGER.value,
            timestamp=datetime.now()
        )

        embed.add_field(
            name="Ação Necessária",
            value="Utilize `/assinar` para renovar sua licença.",
            inline=False
        )

        embed.add_field(
            name="Funções Desbloqueadas",
            value=(
                "✅ /assinar\n"
                "✅ /status\n"
                "✅ /suporte"
            ),
            inline=False
        )

        embed.add_field(
            name="Funções Bloqueadas",
            value=(
                "❌ Loja\n"
                "❌ Dashboard\n"
                "❌ Tickets\n"
                "❌ Estoque\n"
                "❌ Produtos\n"
                "❌ Cupons\n"
                "❌ Pedidos\n"
                "❌ Administração"
            ),
            inline=False
        )

        embed.set_footer(text="LojaEB | Gerenciador de Loja Discord")
        return embed

    @staticmethod
    def create_success_embed(title: str, description: str) -> discord.Embed:
        """Create success embed."""
        embed = discord.Embed(
            title=f"✅ {title}",
            description=description,
            color=EmbedColor.SUCCESS.value,
            timestamp=datetime.now()
        )
        embed.set_footer(text="LojaEB | Gerenciador de Loja Discord")
        return embed

    @staticmethod
    def create_error_embed(title: str, description: str) -> discord.Embed:
        """Create error embed."""
        embed = discord.Embed(
            title=f"❌ {title}",
            description=description,
            color=EmbedColor.DANGER.value,
            timestamp=datetime.now()
        )
        embed.set_footer(text="LojaEB | Gerenciador de Loja Discord")
        return embed

    @staticmethod
    def create_warning_embed(title: str, description: str) -> discord.Embed:
        """Create warning embed."""
        embed = discord.Embed(
            title=f"⚠️ {title}",
            description=description,
            color=EmbedColor.WARNING.value,
            timestamp=datetime.now()
        )
        embed.set_footer(text="LojaEB | Gerenciador de Loja Discord")
        return embed

    @staticmethod
    def create_info_embed(title: str, description: str) -> discord.Embed:
        """Create info embed."""
        embed = discord.Embed(
            title=f"ℹ️ {title}",
            description=description,
            color=EmbedColor.INFO.value,
            timestamp=datetime.now()
        )
        embed.set_footer(text="LojaEB | Gerenciador de Loja Discord")
        return embed

    @staticmethod
    def create_product_embed(
        name: str,
        description: str,
        price: float,
        stock: int,
        image_url: str = None
    ) -> discord.Embed:
        """Create product embed."""
        embed = discord.Embed(
            title=f"📦 {name}",
            description=description,
            color=EmbedColor.PRIMARY.value
        )

        embed.add_field(name="💰 Preço", value=f"R$ {price:.2f}", inline=True)
        embed.add_field(name="📊 Estoque", value=f"{stock} unidades", inline=True)

        if image_url:
            embed.set_image(url=image_url)

        embed.set_footer(text="LojaEB | Gerenciador de Loja Discord")
        return embed

    @staticmethod
    def create_ticket_embed(
        ticket_id: str,
        user: str,
        category: str,
        reason: str
    ) -> discord.Embed:
        """Create ticket embed."""
        embed = discord.Embed(
            title=f"🎫 Ticket #{ticket_id}",
            color=EmbedColor.PRIMARY.value,
            timestamp=datetime.now()
        )

        embed.add_field(name="👤 Aberto por", value=user, inline=True)
        embed.add_field(name="📂 Categoria", value=category, inline=True)
        embed.add_field(name="📝 Motivo", value=reason, inline=False)

        embed.set_footer(text="LojaEB | Gerenciador de Loja Discord")
        return embed

    @staticmethod
    def create_order_embed(
        order_id: str,
        items: list,
        total: float,
        status: str
    ) -> discord.Embed:
        """Create order embed."""
        embed = discord.Embed(
            title=f"🛍️ Pedido #{order_id}",
            color=EmbedColor.PRIMARY.value,
            timestamp=datetime.now()
        )

        items_text = "\n".join([f"• {item['name']} x{item['quantity']}" for item in items])
        embed.add_field(name="📦 Itens", value=items_text, inline=False)
        embed.add_field(name="💰 Total", value=f"R$ {total:.2f}", inline=True)
        embed.add_field(name="📊 Status", value=status, inline=True)

        embed.set_footer(text="LojaEB | Gerenciador de Loja Discord")
        return embed
