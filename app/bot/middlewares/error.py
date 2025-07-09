import traceback
from typing import Any, Awaitable, Callable, Optional, cast

from aiogram.exceptions import TelegramBadRequest
from aiogram.types import BufferedInputFile, ErrorEvent, TelegramObject
from aiogram.types import User as AiogramUser
from loguru import logger

from app.core.constants import APP_CONTAINER_KEY
from app.core.container import AppContainer
from app.core.enums import MediaType, MiddlewareEventType

from .base import EventTypedMiddleware


class ErrorMiddleware(EventTypedMiddleware):
    __event_types__ = [MiddlewareEventType.ERROR]

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        aiogram_user: Optional[AiogramUser] = self._get_aiogram_user(event)
        user_id = str(aiogram_user.id) if aiogram_user else None
        user_name = aiogram_user.full_name if aiogram_user else None

        container: AppContainer = data[APP_CONTAINER_KEY]
        event = cast(ErrorEvent, event)

        logger.exception(f"Update: {event.update}\nException: {event.exception}")

        try:
            text = f"{type(event.exception).__name__}: {str(event.exception)[:1021]}..."
            await container.services.notification.notify_super_dev(
                dev=await container.services.user.get(telegram_id=container.config.bot.dev_id),
                text_key="ntf-event-error",
                media=BufferedInputFile(
                    file=traceback.format_exc().encode(),
                    filename=f"error_{event.update.update_id}.txt",
                ),
                media_type=MediaType.DOCUMENT,
                user=bool(aiogram_user),
                id=user_id,
                name=user_name,
                error=text,
            )

        except TelegramBadRequest as exception:
            logger.warning(f"Failed to send error details: {exception}")
        except Exception as exception:
            logger.error(f"Unexpected error in error handler: {exception}")

        return await handler(event, data)
