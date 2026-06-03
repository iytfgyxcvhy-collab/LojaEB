"""
Shop service for product and order management.
"""

import uuid
from typing import Optional, List, Dict, Any
from bot.database import db_instance, ProductModel, OrderModel, CategoryModel
from bot.utils.logger import get_logger

logger = get_logger("shop_service")


class ShopService:
    """Service for managing shop products and orders."""

    def __init__(self):
        self.db = None

    async def initialize(self):
        """Initialize database connection."""
        self.db = db_instance.get_db()

    # Product methods
    async def create_product(
        self,
        guild_id: int,
        name: str,
        description: str,
        price: float,
        category_id: str,
        stock: int,
        image_url: Optional[str] = None,
        is_digital: bool = False,
        role_id: Optional[int] = None
    ) -> Dict[str, Any]:
        """Create new product."""
        try:
            if not self.db:
                await self.initialize()

            product_id = str(uuid.uuid4())
            product_data = ProductModel.create(
                guild_id, product_id, name, description, price, 
                category_id, stock, image_url, is_digital, role_id
            )
            
            await self.db.products.insert_one(product_data)
            logger.info(f"Product created: {product_id} in guild {guild_id}")
            
            return product_data

        except Exception as e:
            logger.error(f"Error creating product: {str(e)}", exc_info=True)
            raise

    async def get_product(self, product_id: str) -> Optional[Dict[str, Any]]:
        """Get product by ID."""
        try:
            if not self.db:
                await self.initialize()

            return await self.db.products.find_one({"product_id": product_id})

        except Exception as e:
            logger.error(f"Error getting product: {str(e)}", exc_info=True)
            return None

    async def get_products_by_guild(self, guild_id: int) -> List[Dict[str, Any]]:
        """Get all products for guild."""
        try:
            if not self.db:
                await self.initialize()

            cursor = self.db.products.find({
                "guild_id": guild_id,
                "is_active": True
            }).sort("created_at", -1)
            
            return await cursor.to_list(length=None)

        except Exception as e:
            logger.error(f"Error getting guild products: {str(e)}", exc_info=True)
            return []

    async def get_products_by_category(self, guild_id: int, category_id: str) -> List[Dict[str, Any]]:
        """Get products by category."""
        try:
            if not self.db:
                await self.initialize()

            cursor = self.db.products.find({
                "guild_id": guild_id,
                "category_id": category_id,
                "is_active": True
            }).sort("created_at", -1)
            
            return await cursor.to_list(length=None)

        except Exception as e:
            logger.error(f"Error getting category products: {str(e)}", exc_info=True)
            return []

    async def update_product(self, product_id: str, update_data: Dict[str, Any]) -> bool:
        """Update product information."""
        try:
            if not self.db:
                await self.initialize()

            from datetime import datetime
            update_data["updated_at"] = datetime.utcnow()

            result = await self.db.products.update_one(
                {"product_id": product_id},
                {"$set": update_data}
            )
            
            return result.modified_count > 0

        except Exception as e:
            logger.error(f"Error updating product: {str(e)}", exc_info=True)
            raise

    async def delete_product(self, product_id: str) -> bool:
        """Delete/deactivate product."""
        try:
            if not self.db:
                await self.initialize()

            result = await self.db.products.update_one(
                {"product_id": product_id},
                {"$set": {"is_active": False}}
            )
            
            return result.modified_count > 0

        except Exception as e:
            logger.error(f"Error deleting product: {str(e)}", exc_info=True)
            raise

    # Category methods
    async def create_category(
        self,
        guild_id: int,
        name: str,
        description: Optional[str] = None,
        emoji: str = "📂"
    ) -> Dict[str, Any]:
        """Create new product category."""
        try:
            if not self.db:
                await self.initialize()

            category_id = str(uuid.uuid4())
            category_data = CategoryModel.create(guild_id, category_id, name, description, emoji)
            
            await self.db.categories.insert_one(category_data)
            logger.info(f"Category created: {category_id} in guild {guild_id}")
            
            return category_data

        except Exception as e:
            logger.error(f"Error creating category: {str(e)}", exc_info=True)
            raise

    async def get_categories(self, guild_id: int) -> List[Dict[str, Any]]:
        """Get all categories for guild."""
        try:
            if not self.db:
                await self.initialize()

            cursor = self.db.categories.find({
                "guild_id": guild_id,
                "is_active": True
            }).sort("created_at", -1)
            
            return await cursor.to_list(length=None)

        except Exception as e:
            logger.error(f"Error getting categories: {str(e)}", exc_info=True)
            return []

    # Order methods
    async def create_order(
        self,
        guild_id: int,
        user_id: int,
        items: List[Dict[str, Any]],
        total: float
    ) -> Dict[str, Any]:
        """Create new order."""
        try:
            if not self.db:
                await self.initialize()

            order_id = str(uuid.uuid4())
            order_data = OrderModel.create(guild_id, order_id, user_id, items, total)
            
            await self.db.orders.insert_one(order_data)
            logger.info(f"Order created: {order_id} for user {user_id}")
            
            return order_data

        except Exception as e:
            logger.error(f"Error creating order: {str(e)}", exc_info=True)
            raise

    async def get_order(self, order_id: str) -> Optional[Dict[str, Any]]:
        """Get order by ID."""
        try:
            if not self.db:
                await self.initialize()

            return await self.db.orders.find_one({"order_id": order_id})

        except Exception as e:
            logger.error(f"Error getting order: {str(e)}", exc_info=True)
            return None

    async def get_user_orders(self, guild_id: int, user_id: int) -> List[Dict[str, Any]]:
        """Get all orders for user in guild."""
        try:
            if not self.db:
                await self.initialize()

            cursor = self.db.orders.find({
                "guild_id": guild_id,
                "user_id": user_id
            }).sort("created_at", -1)
            
            return await cursor.to_list(length=None)

        except Exception as e:
            logger.error(f"Error getting user orders: {str(e)}", exc_info=True)
            return []

    async def update_order_status(self, order_id: str, status: str) -> bool:
        """Update order status."""
        try:
            if not self.db:
                await self.initialize()

            from datetime import datetime
            
            update_data = {
                "status": status,
                "updated_at": datetime.utcnow()
            }
            
            if status == "delivered":
                update_data["delivered_at"] = datetime.utcnow()
            
            result = await self.db.orders.update_one(
                {"order_id": order_id},
                {"$set": update_data}
            )
            
            return result.modified_count > 0

        except Exception as e:
            logger.error(f"Error updating order status: {str(e)}", exc_info=True)
            raise

    # Stock management
    async def update_stock(self, product_id: str, quantity: int) -> bool:
        """Update product stock."""
        try:
            if not self.db:
                await self.initialize()

            result = await self.db.products.update_one(
                {"product_id": product_id},
                {"$inc": {"stock": quantity}}
            )
            
            return result.modified_count > 0

        except Exception as e:
            logger.error(f"Error updating stock: {str(e)}", exc_info=True)
            raise

    async def get_stock(self, product_id: str) -> Optional[int]:
        """Get product stock quantity."""
        try:
            if not self.db:
                await self.initialize()

            product = await self.db.products.find_one({"product_id": product_id})
            return product.get("stock") if product else None

        except Exception as e:
            logger.error(f"Error getting stock: {str(e)}", exc_info=True)
            return None
