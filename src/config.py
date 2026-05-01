"""Configuration for Taskchamp Capture Bot."""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(env_path)

# Telegram settings
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")

# Support multiple allowed user IDs (comma-separated)
# Example: ALLOWED_USER_IDS=123456789,987654321
_allowed_ids_str = os.getenv("ALLOWED_USER_IDS", "")
if _allowed_ids_str:
    ALLOWED_USER_IDS = [int(uid.strip()) for uid in _allowed_ids_str.split(",") if uid.strip()]
else:
    # Fallback to single user ID for backward compatibility
    _single_id = os.getenv("ALLOWED_USER_ID", "")
    ALLOWED_USER_IDS = [int(_single_id)] if _single_id else []

# Taskwarrior settings
TASKRC_PATH = os.getenv("TASKRC_PATH", str(Path.home() / ".taskrc"))
TASK_DATA_DIR = Path(os.getenv("TASK_DATA_DIR", str(Path.home() / ".task")))

# Logging
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# Validation
if not TELEGRAM_BOT_TOKEN:
    raise ValueError("TELEGRAM_BOT_TOKEN environment variable is required")

if not ALLOWED_USER_IDS:
    raise ValueError("ALLOWED_USER_IDS environment variable is required (comma-separated list of Telegram user IDs)")
