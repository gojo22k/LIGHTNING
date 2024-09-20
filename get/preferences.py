# preferences.py
from helper.database import db
from config import Config
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def get_rename_preference(user_id):
    """Fetch the renaming preference for the user."""
    try:
        # Fetch the auto renaming status from the database
        auto_rename_status = await db.get_auto_rename_status(user_id)

        # Log the renaming preference
        if auto_rename_status == "✅":
            logger.info(f"User {user_id} has auto renaming enabled.")
            return "auto"
        else:
            logger.info(f"User {user_id} has manual renaming enabled.")
            return "manual"
    except Exception as e:
        logger.error(f"Error fetching renaming preference for user {user_id}: {e}")
        return "manual"  # Default to manual if there's an error
