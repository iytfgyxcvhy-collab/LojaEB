"""
Database connection and configuration.
"""

import os
import motor.motor_asyncio
from pymongo.errors import ServerSelectionTimeoutError
from bot.utils.logger import get_logger

logger = get_logger("database")


class Database:
    """MongoDB database connection manager."""

    _instance = None
    _client = None
    _db = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    async def connect(self):
        """Connect to MongoDB."""
        try:
            mongodb_uri = os.getenv("MONGODB_URI")
            database_name = os.getenv("DATABASE_NAME", "LojaEB")

            if not mongodb_uri:
                raise ValueError("MONGODB_URI environment variable not set")

            self._client = motor.motor_asyncio.AsyncIOMotorClient(mongodb_uri)
            self._db = self._client[database_name]

            # Test connection
            await self._client.admin.command('ping')
            logger.info(f"✅ Connected to MongoDB: {database_name}")
            await self.create_indexes()

        except ServerSelectionTimeoutError:
            logger.error("❌ Failed to connect to MongoDB - Connection timeout")
            raise
        except Exception as e:
            logger.error(f"❌ Failed to connect to MongoDB: {str(e)}")
            raise

    async def disconnect(self):
        """Disconnect from MongoDB."""
        if self._client:
            self._client.close()
            logger.info("✅ Disconnected from MongoDB")

    def get_db(self):
        """Get database instance."""
        if self._db is None:
            raise RuntimeError("Database not connected. Call connect() first.")
        return self._db

    def get_client(self):
        """Get MongoDB client instance."""
        if self._client is None:
            raise RuntimeError("Database not connected. Call connect() first.")
        return self._client

    async def get_collection(self, collection_name: str):
        """Get collection by name."""
        return self._db[collection_name]

    async def create_indexes(self):
        """Create necessary indexes for performance."""
        try:
            db = self.get_db()

            # Guilds indexes
            await db.guilds.create_index("guild_id", unique=True)
            await db.guilds.create_index("created_at")

            # Licenses indexes
            await db.licenses.create_index("guild_id", unique=True)
            await db.licenses.create_index("expiration_date")
            await db.licenses.create_index("status")

            # Products indexes
            await db.products.create_index("guild_id")
            await db.products.create_index("category_id")
            await db.products.create_index("product_id", unique=True)

            # Orders indexes
            await db.orders.create_index("guild_id")
            await db.orders.create_index("user_id")
            await db.orders.create_index("order_id", unique=True)
            await db.orders.create_index("created_at")

            # Payments indexes
            await db.payments.create_index("guild_id")
            await db.payments.create_index("order_id")
            await db.payments.create_index("status")
            await db.payments.create_index("created_at")

            # Coupons indexes
            await db.coupons.create_index("code", unique=True)
            await db.coupons.create_index("guild_id")

            # Tickets indexes
            await db.tickets.create_index("guild_id")
            await db.tickets.create_index("ticket_id", unique=True)
            await db.tickets.create_index("user_id")

            # Logs indexes
            await db.logs.create_index("guild_id")
            await db.logs.create_index("timestamp")
            await db.logs.create_index([("timestamp", -1)], expireAfterSeconds=86400*30)  # 30 days

            logger.info("✅ Database indexes created successfully")

        except Exception as e:
            logger.error(f"❌ Error creating indexes: {str(e)}")
            raise


# Singleton instance
db_instance = Database()


async def get_database():
    """Get database instance."""
    return db_instance.get_db()


async def get_database_client():
    """Get MongoDB client."""
    return db_instance.get_client()
