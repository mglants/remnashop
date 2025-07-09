from typing import Any, Awaitable, Callable

from aiogram.types import TelegramObject

from app.core.constants import APP_CONTAINER_KEY, USER_KEY
from app.core.container import AppContainer
from app.core.enums import MiddlewareEventType
from app.db.models.dto import UserDto

from .base import EventTypedMiddleware


class MaintenanceMiddleware(EventTypedMiddleware):
    __event_types__ = [MiddlewareEventType.MESSAGE, MiddlewareEventType.CALLBACK_QUERY]

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        container: AppContainer = data[APP_CONTAINER_KEY]
        user: UserDto = data[USER_KEY]

        maintenance_service = container.services.maintenance
        notification_service = container.services.notification
        access_allowed = await maintenance_service.check_access(user=user, event=event)

        if not access_allowed:
            await notification_service.notify_user(
                user=user,
                text_key="ntf-maintenance-denied-global",
            )
            return

        return await handler(event, data)
