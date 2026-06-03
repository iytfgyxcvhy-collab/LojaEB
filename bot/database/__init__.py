"""
Database package initialization.
"""

from bot.database.connection import Database, db_instance, get_database, get_database_client
from bot.database.models import (
    GuildModel,
    LicenseModel,
    ProductModel,
    OrderModel,
    PaymentModel,
    CouponModel,
    TicketModel,
    LogModel,
    UserModel,
    CategoryModel
)

__all__ = [
    "Database",
    "db_instance",
    "get_database",
    "get_database_client",
    "GuildModel",
    "LicenseModel",
    "ProductModel",
    "OrderModel",
    "PaymentModel",
    "CouponModel",
    "TicketModel",
    "LogModel",
    "UserModel",
    "CategoryModel"
]
