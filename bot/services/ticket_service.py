"""
Ticket service for ticket management.
"""

import uuid
from typing import Optional, List, Dict, Any
from bot.database import db_instance, TicketModel
from bot.utils.logger import get_logger

logger = get_logger("ticket_service")


class TicketService:
    """Service for managing support tickets."""

    def __init__(self):
        self.db = None

    async def initialize(self):
        """Initialize database connection."""
        self.db = db_instance.get_db()

    async def create_ticket(
        self,
        guild_id: int,
        user_id: int,
        category: str,
        reason: str,
        channel_id: int
    ) -> Dict[str, Any]:
        """Create new support ticket."""
        try:
            if not self.db:
                await self.initialize()

            ticket_id = str(uuid.uuid4())
            ticket_data = TicketModel.create(
                guild_id, ticket_id, user_id, category, reason, channel_id
            )
            
            await self.db.tickets.insert_one(ticket_data)
            logger.info(f"Ticket created: {ticket_id} for user {user_id}")
            
            return ticket_data

        except Exception as e:
            logger.error(f"Error creating ticket: {str(e)}", exc_info=True)
            raise

    async def get_ticket(self, ticket_id: str) -> Optional[Dict[str, Any]]:
        """Get ticket by ID."""
        try:
            if not self.db:
                await self.initialize()

            return await self.db.tickets.find_one({"ticket_id": ticket_id})

        except Exception as e:
            logger.error(f"Error getting ticket: {str(e)}", exc_info=True)
            return None

    async def get_user_tickets(self, guild_id: int, user_id: int) -> List[Dict[str, Any]]:
        """Get all tickets for user in guild."""
        try:
            if not self.db:
                await self.initialize()

            cursor = self.db.tickets.find({
                "guild_id": guild_id,
                "user_id": user_id
            }).sort("created_at", -1)
            
            return await cursor.to_list(length=None)

        except Exception as e:
            logger.error(f"Error getting user tickets: {str(e)}", exc_info=True)
            return []

    async def get_open_tickets(self, guild_id: int) -> List[Dict[str, Any]]:
        """Get all open tickets in guild."""
        try:
            if not self.db:
                await self.initialize()

            cursor = self.db.tickets.find({
                "guild_id": guild_id,
                "status": "open"
            }).sort("created_at", -1)
            
            return await cursor.to_list(length=None)

        except Exception as e:
            logger.error(f"Error getting open tickets: {str(e)}", exc_info=True)
            return []

    async def close_ticket(self, ticket_id: str) -> bool:
        """Close support ticket."""
        try:
            if not self.db:
                await self.initialize()

            from datetime import datetime
            
            result = await self.db.tickets.update_one(
                {"ticket_id": ticket_id},
                {"$set": {"status": "closed", "closed_at": datetime.utcnow()}}
            )
            
            if result.modified_count > 0:
                logger.info(f"Ticket closed: {ticket_id}")
                return True
            
            return False

        except Exception as e:
            logger.error(f"Error closing ticket: {str(e)}", exc_info=True)
            raise

    async def add_transcript_message(self, ticket_id: str, user_id: int, message: str) -> bool:
        """Add message to ticket transcript."""
        try:
            if not self.db:
                await self.initialize()

            from datetime import datetime
            
            result = await self.db.tickets.update_one(
                {"ticket_id": ticket_id},
                {"$push": {"transcript": {
                    "user_id": user_id,
                    "message": message,
                    "timestamp": datetime.utcnow()
                }}}
            )
            
            return result.modified_count > 0

        except Exception as e:
            logger.error(f"Error adding transcript message: {str(e)}", exc_info=True)
            raise

    async def get_ticket_transcript(self, ticket_id: str) -> Optional[List[Dict[str, Any]]]:
        """Get ticket transcript."""
        try:
            if not self.db:
                await self.initialize()

            ticket = await self.db.tickets.find_one({"ticket_id": ticket_id})
            return ticket.get("transcript", []) if ticket else None

        except Exception as e:
            logger.error(f"Error getting ticket transcript: {str(e)}", exc_info=True)
            return None
