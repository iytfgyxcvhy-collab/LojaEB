"""
Subscription service for license management.
"""

from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from bot.database import db_instance, LicenseModel
from bot.utils.logger import get_logger

logger = get_logger("subscription_service")


class SubscriptionService:
    """Service for managing subscriptions and licenses."""

    def __init__(self):
        self.db = None

    async def initialize(self):
        """Initialize database connection."""
        self.db = db_instance.get_db()

    async def create_subscription(self, guild_id: int, plan: str) -> Dict[str, Any]:
        """Create new subscription for guild."""
        try:
            if not self.db:
                await self.initialize()

            # Check if guild already has subscription
            existing = await self.db.licenses.find_one({"guild_id": guild_id})
            
            license_data = LicenseModel.create(guild_id, plan)
            
            if existing:
                # Update existing license
                await self.db.licenses.update_one(
                    {"guild_id": guild_id},
                    {"$set": license_data}
                )
                logger.info(f"License updated for guild {guild_id} - Plan: {plan}")
            else:
                # Create new license
                await self.db.licenses.insert_one(license_data)
                logger.info(f"License created for guild {guild_id} - Plan: {plan}")
            
            return license_data

        except Exception as e:
            logger.error(f"Error creating subscription: {str(e)}", exc_info=True)
            raise

    async def check_license(self, guild_id: int) -> bool:
        """Check if guild has active license."""
        try:
            if not self.db:
                await self.initialize()

            license_data = await self.db.licenses.find_one({"guild_id": guild_id})
            
            if not license_data:
                return False
            
            if license_data.get("status") != "active":
                return False
            
            # Check expiration
            expiration_date = license_data.get("expiration_date")
            if expiration_date and expiration_date < datetime.utcnow():
                # License expired
                await self.db.licenses.update_one(
                    {"guild_id": guild_id},
                    {"$set": {"status": "expired"}}
                )
                logger.info(f"License expired for guild {guild_id}")
                return False
            
            return True

        except Exception as e:
            logger.error(f"Error checking license: {str(e)}", exc_info=True)
            return False

    async def get_license_info(self, guild_id: int) -> Optional[Dict[str, Any]]:
        """Get license information for guild."""
        try:
            if not self.db:
                await self.initialize()

            return await self.db.licenses.find_one({"guild_id": guild_id})

        except Exception as e:
            logger.error(f"Error getting license info: {str(e)}", exc_info=True)
            return None

    async def renew_subscription(self, guild_id: int, plan: str) -> Dict[str, Any]:
        """Renew subscription for guild."""
        try:
            if not self.db:
                await self.initialize()

            license_data = LicenseModel.create(guild_id, plan)
            
            await self.db.licenses.update_one(
                {"guild_id": guild_id},
                {"$set": license_data, "$push": {"renewal_history": datetime.utcnow()}}
            )
            
            logger.info(f"License renewed for guild {guild_id} - Plan: {plan}")
            return license_data

        except Exception as e:
            logger.error(f"Error renewing subscription: {str(e)}", exc_info=True)
            raise

    async def cancel_subscription(self, guild_id: int) -> bool:
        """Cancel subscription for guild."""
        try:
            if not self.db:
                await self.initialize()

            result = await self.db.licenses.update_one(
                {"guild_id": guild_id},
                {"$set": {"status": "canceled", "canceled_at": datetime.utcnow()}}
            )
            
            if result.modified_count > 0:
                logger.info(f"License canceled for guild {guild_id}")
                return True
            
            return False

        except Exception as e:
            logger.error(f"Error canceling subscription: {str(e)}", exc_info=True)
            raise

    async def set_auto_renew(self, guild_id: int, auto_renew: bool) -> bool:
        """Set auto-renewal for subscription."""
        try:
            if not self.db:
                await self.initialize()

            result = await self.db.licenses.update_one(
                {"guild_id": guild_id},
                {"$set": {"auto_renew": auto_renew}}
            )
            
            return result.modified_count > 0

        except Exception as e:
            logger.error(f"Error setting auto-renew: {str(e)}", exc_info=True)
            raise

    async def get_expiration_date(self, guild_id: int) -> Optional[datetime]:
        """Get license expiration date."""
        try:
            if not self.db:
                await self.initialize()

            license_data = await self.db.licenses.find_one({"guild_id": guild_id})
            
            if license_data:
                return license_data.get("expiration_date")
            
            return None

        except Exception as e:
            logger.error(f"Error getting expiration date: {str(e)}", exc_info=True)
            return None

    async def get_days_until_expiration(self, guild_id: int) -> Optional[int]:
        """Get number of days until license expiration."""
        try:
            expiration_date = await self.get_expiration_date(guild_id)
            
            if expiration_date:
                days_left = (expiration_date - datetime.utcnow()).days
                return max(0, days_left)
            
            return None

        except Exception as e:
            logger.error(f"Error calculating days until expiration: {str(e)}", exc_info=True)
            return None
