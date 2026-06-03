"""
Payment service for payment processing.
"""

import uuid
import qrcode
import io
from typing import Optional, Dict, Any
from bot.database import db_instance, PaymentModel
from bot.utils.logger import get_logger

logger = get_logger("payment_service")


class PaymentService:
    """Service for managing payments and transactions."""

    def __init__(self):
        self.db = None

    async def initialize(self):
        """Initialize database connection."""
        self.db = db_instance.get_db()

    async def create_payment(
        self,
        guild_id: int,
        order_id: str,
        user_id: int,
        amount: float,
        payment_method: str = "pix"
    ) -> Dict[str, Any]:
        """Create new payment record."""
        try:
            if not self.db:
                await self.initialize()

            payment_data = PaymentModel.create(
                guild_id, order_id, user_id, amount, payment_method
            )
            
            await self.db.payments.insert_one(payment_data)
            logger.info(f"Payment created for order {order_id}")
            
            return payment_data

        except Exception as e:
            logger.error(f"Error creating payment: {str(e)}", exc_info=True)
            raise

    async def get_payment(self, payment_id: str) -> Optional[Dict[str, Any]]:
        """Get payment by ID."""
        try:
            if not self.db:
                await self.initialize()

            return await self.db.payments.find_one({"_id": payment_id})

        except Exception as e:
            logger.error(f"Error getting payment: {str(e)}", exc_info=True)
            return None

    async def get_order_payment(self, order_id: str) -> Optional[Dict[str, Any]]:
        """Get payment by order ID."""
        try:
            if not self.db:
                await self.initialize()

            return await self.db.payments.find_one({"order_id": order_id})

        except Exception as e:
            logger.error(f"Error getting order payment: {str(e)}", exc_info=True)
            return None

    async def update_payment_status(self, order_id: str, status: str, transaction_id: Optional[str] = None) -> bool:
        """Update payment status."""
        try:
            if not self.db:
                await self.initialize()

            from datetime import datetime
            
            update_data = {
                "status": status,
                "updated_at": datetime.utcnow()
            }
            
            if transaction_id:
                update_data["transaction_id"] = transaction_id
            
            result = await self.db.payments.update_one(
                {"order_id": order_id},
                {"$set": update_data}
            )
            
            if result.modified_count > 0:
                logger.info(f"Payment status updated: {order_id} -> {status}")
                return True
            
            return False

        except Exception as e:
            logger.error(f"Error updating payment status: {str(e)}", exc_info=True)
            raise

    def generate_pix_qr_code(self, pix_key: str) -> bytes:
        """Generate QR code for PIX payment."""
        try:
            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(pix_key)
            qr.make(fit=True)

            img = qr.make_image(fill_color="black", back_color="white")
            
            # Convert to bytes
            img_io = io.BytesIO()
            img.save(img_io, 'PNG')
            img_io.seek(0)
            
            return img_io.getvalue()

        except Exception as e:
            logger.error(f"Error generating QR code: {str(e)}", exc_info=True)
            raise

    async def get_user_payment_history(self, guild_id: int, user_id: int) -> list:
        """Get payment history for user."""
        try:
            if not self.db:
                await self.initialize()

            cursor = self.db.payments.find({
                "guild_id": guild_id,
                "user_id": user_id
            }).sort("created_at", -1)
            
            return await cursor.to_list(length=None)

        except Exception as e:
            logger.error(f"Error getting payment history: {str(e)}", exc_info=True)
            return []

    async def get_guild_revenue(self, guild_id: int) -> float:
        """Get total revenue for guild."""
        try:
            if not self.db:
                await self.initialize()

            pipeline = [
                {"$match": {"guild_id": guild_id, "status": "approved"}},
                {"$group": {"_id": None, "total": {"$sum": "$amount"}}}
            ]
            
            result = await self.db.payments.aggregate(pipeline).to_list(length=1)
            return result[0]["total"] if result else 0.0

        except Exception as e:
            logger.error(f"Error calculating revenue: {str(e)}", exc_info=True)
            return 0.0
