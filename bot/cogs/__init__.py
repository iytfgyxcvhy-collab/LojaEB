"""
Cogs package initialization.
"""

import os
import sys
from pathlib import Path


async def load_cogs(bot):
    """Load all cogs from the cogs directory."""
    cogs_dir = Path(__file__).parent
    
    for filename in os.listdir(cogs_dir):
        if filename.endswith(".py") and not filename.startswith("_"):
            cog_name = filename[:-3]
            try:
                await bot.load_extension(f"bot.cogs.{cog_name}")
                print(f"✅ Loaded cog: {cog_name}")
            except Exception as e:
                print(f"❌ Failed to load cog {cog_name}: {str(e)}", file=sys.stderr)
                raise
