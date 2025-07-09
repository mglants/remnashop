from typing import Any, Awaitable, Callable, Optional

from aiogram.types import TelegramObject
from fluent.runtime import FluentLocalization
from loguru import logger

from app.core.constants import I18N_FORMATTER_KEY, USER_KEY
from app.core.enums import Locale, MiddlewareEventType
from app.core.utils.formatters import format_log_user
from app.core.utils.types import I18nFormatter
from app.db.models.dto import UserDto

from .base import EventTypedMiddleware


class I18nMiddleware(EventTypedMiddleware):
    __event_types__ = [
        MiddlewareEventType.MESSAGE,
        MiddlewareEventType.CALLBACK_QUERY,
        MiddlewareEventType.ERROR,
        MiddlewareEventType.AIOGD_UPDATE,
    ]

    def __init__(
        self,
        locales: dict[Locale, FluentLocalization],
        default_locale: Locale,
    ) -> None:
        self.locales = locales
        self.default_locale = default_locale
        logger.debug(f"Available locales: {list(locales.keys())}")
        super().__init__()

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        user: UserDto = data[USER_KEY]
        data[I18N_FORMATTER_KEY] = self.get_formatter(user=user)
        return await handler(event, data)

    def get_locale(
        self,
        user: Optional[UserDto] = None,
        locale: Optional[Locale] = None,
    ) -> FluentLocalization:
        target_locale: Locale

        if locale is not None:
            target_locale = locale
            # logger.debug(f"Using explicitly provided locale: '{target_locale}'")
        elif user is not None and user.language in self.locales:
            target_locale = Locale(user.language)
            # logger.debug(f"{format_log_user(user)} Using locale '{target_locale}'")
        else:
            target_locale = self.default_locale

            if user is None:
                logger.debug(
                    f"User not provided or user's language not supported. "
                    f"Using default locale: '{self.default_locale}'"
                )
            else:
                logger.warning(
                    f"Locale '{user.language}' for user '{user.telegram_id}' not supported. "
                    f"Using default locale: '{self.default_locale}'"
                )

        if target_locale not in self.locales:
            logger.error(
                f"Resolved locale '{target_locale}' is not available. "
                f"Falling back to default: '{self.default_locale}'"
            )
            return self.locales[self.default_locale]

        return self.locales[target_locale]

    def get_formatter(
        self,
        user: Optional[UserDto] = None,
        locale: Optional[Locale] = None,
    ) -> I18nFormatter:
        return self.get_locale(user=user, locale=locale).format_value
