"""Telegram bot for capturing tasks to Taskwarrior."""
import logging
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)

from config import TELEGRAM_BOT_TOKEN, ALLOWED_USER_IDS, LOG_LEVEL
from task_service import add_task, sync_tasks

# Configure logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=getattr(logging, LOG_LEVEL.upper())
)
logger = logging.getLogger(__name__)

# Error help messages for common mistakes
DATE_HELP = """💡 Try:
• today, tomorrow, eod
• monday, next week  
• 2025-05-01, May 1"""

PRIORITY_HELP = """💡 Priority must be H, M, or L
Examples:
• priority:H
• priority:M"""


async def is_authorized(update: Update) -> bool:
    """Check if user is authorized to use the bot."""
    user_id = update.effective_user.id
    return user_id in ALLOWED_USER_IDS


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /start command - minimal help."""
    if not await is_authorized(update):
        return
    
    await update.message.reply_text(
        "Send me any task and I'll add it to Taskwarrior.\n"
        "Example: Buy milk due:today +groceries"
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle incoming messages - capture tasks."""
    if not await is_authorized(update):
        # Silent ignore for unauthorized users
        logger.warning(f"Unauthorized access attempt from user {update.effective_user.id}")
        return
    
    task_text = update.message.text.strip()
    
    if not task_text:
        return
    
    # TODO: Future enhancement - Voice message support
    # if update.message.voice:
    #     # Implement speech-to-text conversion
    #     # task_text = await convert_voice_to_text(update.message.voice)
    #     pass
    
    logger.info(f"Adding task from user {update.effective_user.id}: {task_text}")
    
    # Step 1: Add the task
    add_result = add_task(task_text)
    
    if not add_result.success:
        # Format error message with helpful suggestions
        error_response = format_error_response(add_result)
        await update.message.reply_text(error_response)
        return
    
    # Step 2: Sync with server
    sync_result = sync_tasks()
    
    # Build response
    response_parts = ["✅ Added"]
    
    if sync_result.success:
        response_parts.append("\n\nSynced ✓")
    else:
        response_parts.append("\n\n⚠️ Saved locally (sync failed)")
        logger.warning(f"Sync failed: {sync_result.message}")
    
    await update.message.reply_text("".join(response_parts))


def format_error_response(result) -> str:
    """Format error message with helpful suggestions."""
    base_error = f"⚠️ Couldn't add task\n\n{result.message}"
    
    if result.error_type == "invalid_date":
        return f"{base_error}\n\n{DATE_HELP}"
    elif result.error_type == "invalid_priority":
        return f"{base_error}\n\n{PRIORITY_HELP}"
    
    return base_error


def main() -> None:
    """Start the bot."""
    logger.info("Starting Taskchamp Capture Bot...")
    logger.info(f"Authorized users: {ALLOWED_USER_IDS}")
    
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    
    # Handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # TODO: Future enhancement - Voice message support
    # application.add_handler(MessageHandler(filters.VOICE, handle_voice))
    
    # Run the bot until Ctrl-C is pressed
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
