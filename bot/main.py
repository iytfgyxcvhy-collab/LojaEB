"""
Main bot entry point.
"""

import os
import asyncio
import discord
from discord.ext import commands
from dotenv import load_dotenv
from bot.database import db_instance
from bot.utils.logger import get_logger
from bot.cogs import load_cogs

# Load environment variables
load_dotenv()

# Initialize logger
logger = get_logger("main")

# Bot configuration
INTENTS = discord.Intents.default()
INTENTS.message_content = True
INTENTS.members = True
INTENTS.guilds = True

bot = commands.Bot(
    command_prefix="!",
    intents=INTENTS,
    help_command=None
)


async def initialize_bot():
    """Initialize bot systems."""
    try:
        # Connect to database
        await db_instance.connect()
        logger.info("✅ Database initialized")
        
        # Load cogs
        await load_cogs(bot)
        logger.info("✅ All cogs loaded")
        
    except Exception as e:
        logger.error(f"❌ Failed to initialize bot: {str(e)}", exc_info=True)
        raise


async def main():
    """Main bot function."""
    try:
        # Initialize bot systems
        await initialize_bot()
        
        # Start bot
        token = os.getenv("DISCORD_TOKEN")
        if not token:
            raise ValueError("DISCORD_TOKEN not set in environment variables")
        
        logger.info("🚀 Starting bot...")
        await bot.start(token)
        
    except Exception as e:
        logger.error(f"❌ Fatal error: {str(e)}", exc_info=True)
        raise
    finally:
        await db_instance.disconnect()


@bot.event
async def on_ready():
    """Bot ready event."""
    logger.info(f"✅ Bot connected as {bot.user}")
    logger.info(f"✅ Syncing commands...")
    await bot.tree.sync()
    logger.info(f"✅ Commands synced!")


if __name__ == "__main__":
    asyncio.run(main())
