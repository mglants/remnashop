from typing import Any, Awaitable, Callable

from aiogram.types import TelegramObject
from cachetools import TTLCache
from loguru import logger

from app.core.constants import APP_CONTAINER_KEY, USER_KEY
from app.core.container import AppContainer
from app.core.enums import MiddlewareEventType
from app.core.utils.formatters import format_log_user
from app.db.models.dto import UserDto

from .base import EventTypedMiddleware


class ThrottlingMiddleware(EventTypedMiddleware):
    __event_types__ = [MiddlewareEventType.MESSAGE, MiddlewareEventType.CALLBACK_QUERY]

    def __init__(self, ttl: float = 0.5) -> None:
        self.cache: TTLCache[int, Any] = TTLCache(maxsize=10_000, ttl=ttl)
        super().__init__()

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        container: AppContainer = data[APP_CONTAINER_KEY]
        user: UserDto = data[USER_KEY]

        if user.telegram_id in self.cache:
            await container.services.notification.notify_user(
                user=user,
                text_key="ntf-throttling-many-requests",
            )
            logger.warning(f"{format_log_user(user)} Throttled")
            return

        self.cache[user.telegram_id] = None
        return await handler(event, data)
