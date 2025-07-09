from typing import Final, cast

from aiogram import Bot, F, Router
from aiogram.types import CallbackQuery, Message
from loguru import logger

from app.bot.states import Notification
from app.core.utils.formatters import format_log_user
from app.db.models.dto import UserDto

router: Final[Router] = Router(name=__name__)


# TODO: Move logic to notification service
@router.callback_query(F.data.startswith(Notification.CLOSE.state))
async def callback_close_notification(callback: CallbackQuery, bot: Bot, user: UserDto) -> None:
    notification: Message = cast(Message, callback.message)
    notification_id = notification.message_id

    logger.info(f"{format_log_user(user)} Closed notification '{notification_id}'")

    try:
        await notification.delete()
        logger.debug(f"Notification '{notification_id}' for user '{user.telegram_id}' deleted")
    except Exception as exception:
        logger.error(f"Failed to delete notification '{notification_id}'. Error: {exception}")

        try:
            logger.debug(f"Attempting to remove keyboard from notification '{notification_id}'")
            await bot.edit_message_reply_markup(
                chat_id=notification.chat.id,
                message_id=notification.message_id,
                reply_markup=None,
            )
            logger.debug(f"Keyboard removed from notification '{notification_id}'")
        except Exception as exception:
            logger.error(
                f"Failed to remove keyboard from notification '{notification_id}'. "
                f"Error: {exception}"
            )
