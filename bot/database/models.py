"""
Database models and schemas.
"""

from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta


class GuildModel:
    """Guild/Server model."""
    
    @staticmethod
    def create(guild_id: int, guild_name: str, owner_id: int) -> Dict[str, Any]:
        """Create new guild document."""
        return {
            "guild_id": guild_id,
            "guild_name": guild_name,
            "owner_id": owner_id,
            "created_at": datetime.utcnow(),
            "settings": {
                "prefix": "!",
                "language": "pt-BR",
                "timezone": "America/Sao_Paulo"
            },
            "is_active": True
        }


class LicenseModel:
    """License/Subscription model."""
    
    PLANS = {
        "daily": {"days": 1, "price": 9.99},
        "monthly": {"days": 30, "price": 29.99},
        "quarterly": {"days": 90, "price": 79.99}
    }

    @staticmethod
    def create(guild_id: int, plan: str) -> Dict[str, Any]:
        """Create new license document."""
        if plan not in LicenseModel.PLANS:
            raise ValueError(f"Invalid plan: {plan}")
        
        plan_info = LicenseModel.PLANS[plan]
        created_at = datetime.utcnow()
        expiration_date = created_at + timedelta(days=plan_info["days"])
        
        return {
            "guild_id": guild_id,
            "plan": plan,
            "price": plan_info["price"],
            "status": "active",
            "created_at": created_at,
            "expiration_date": expiration_date,
            "renewal_date": None,
            "auto_renew": False
        }


class ProductModel:
    """Product model."""

    @staticmethod
    def create(
        guild_id: int,
        product_id: str,
        name: str,
        description: str,
        price: float,
        category_id: str,
        stock: int,
        image_url: Optional[str] = None,
        is_digital: bool = False,
        role_id: Optional[int] = None
    ) -> Dict[str, Any]:
        """Create new product document."""
        return {
            "guild_id": guild_id,
            "product_id": product_id,
            "name": name,
            "description": description,
            "price": price,
            "category_id": category_id,
            "stock": stock,
            "image_url": image_url,
            "is_digital": is_digital,
            "role_id": role_id,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
            "is_active": True
        }


class OrderModel:
    """Order model."""

    @staticmethod
    def create(
        guild_id: int,
        order_id: str,
        user_id: int,
        items: List[Dict[str, Any]],
        total: float
    ) -> Dict[str, Any]:
        """Create new order document."""
        return {
            "guild_id": guild_id,
            "order_id": order_id,
            "user_id": user_id,
            "items": items,
            "total": total,
            "status": "pending",
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
            "payment_id": None,
            "delivered_at": None
        }


class PaymentModel:
    """Payment model."""

    @staticmethod
    def create(
        guild_id: int,
        order_id: str,
        user_id: int,
        amount: float,
        payment_method: str = "pix"
    ) -> Dict[str, Any]:
        """Create new payment document."""
        return {
            "guild_id": guild_id,
            "order_id": order_id,
            "user_id": user_id,
            "amount": amount,
            "payment_method": payment_method,
            "status": "pending",
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
            "transaction_id": None,
            "qr_code": None,
            "pix_key": None
        }


class CouponModel:
    """Coupon model."""

    @staticmethod
    def create(
        guild_id: int,
        code: str,
        discount: float,
        max_uses: Optional[int] = None,
        expiration_date: Optional[datetime] = None
    ) -> Dict[str, Any]:
        """Create new coupon document."""
        return {
            "guild_id": guild_id,
            "code": code,
            "discount": discount,
            "max_uses": max_uses,
            "current_uses": 0,
            "expiration_date": expiration_date,
            "created_at": datetime.utcnow(),
            "is_active": True
        }


class TicketModel:
    """Ticket model."""

    CATEGORIES = ["suporte", "compras", "parcerias", "denuncias", "duvidas"]

    @staticmethod
    def create(
        guild_id: int,
        ticket_id: str,
        user_id: int,
        category: str,
        reason: str,
        channel_id: int
    ) -> Dict[str, Any]:
        """Create new ticket document."""
        if category not in TicketModel.CATEGORIES:
            raise ValueError(f"Invalid category: {category}")

        return {
            "guild_id": guild_id,
            "ticket_id": ticket_id,
            "user_id": user_id,
            "category": category,
            "reason": reason,
            "channel_id": channel_id,
            "status": "open",
            "created_at": datetime.utcnow(),
            "closed_at": None,
            "transcript": []
        }


class LogModel:
    """Log/Audit model."""

    @staticmethod
    def create(
        guild_id: int,
        user_id: int,
        action: str,
        details: Dict[str, Any],
        ip_address: Optional[str] = None
    ) -> Dict[str, Any]:
        """Create new log document."""
        return {
            "guild_id": guild_id,
            "user_id": user_id,
            "action": action,
            "details": details,
            "timestamp": datetime.utcnow(),
            "ip_address": ip_address
        }


class UserModel:
    """User model."""

    @staticmethod
    def create(
        user_id: int,
        username: str,
        email: Optional[str] = None,
        avatar_url: Optional[str] = None
    ) -> Dict[str, Any]:
        """Create new user document."""
        return {
            "user_id": user_id,
            "username": username,
            "email": email,
            "avatar_url": avatar_url,
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow(),
            "total_spent": 0.0,
            "total_orders": 0
        }


class CategoryModel:
    """Product category model."""

    @staticmethod
    def create(
        guild_id: int,
        category_id: str,
        name: str,
        description: Optional[str] = None,
        emoji: str = "📂"
    ) -> Dict[str, Any]:
        """Create new category document."""
        return {
            "guild_id": guild_id,
            "category_id": category_id,
            "name": name,
            "description": description,
            "emoji": emoji,
            "created_at": datetime.utcnow(),
            "is_active": True
        }
