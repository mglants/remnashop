from typing import NamedTuple, cast

from fluent.runtime import FluentLocalization, FluentResourceLoader

from app.bot.middlewares import (
    ErrorMiddleware,
    GarbageMiddleware,
    I18nMiddleware,
    MaintenanceMiddleware,
    ThrottlingMiddleware,
    UserMiddleware,
)
from app.bot.middlewares.base import EventTypedMiddleware
from app.core.config import AppConfig
from app.core.constants import LOCALES_DIR, RESOURCE_I18N


class Middlewares(NamedTuple):
    outer: list[EventTypedMiddleware]
    inner: list[EventTypedMiddleware]

    def get_i18n_middleware(self) -> I18nMiddleware:
        if not self.inner:
            raise ValueError("Inner middleware list is empty")
        return cast(I18nMiddleware, self.inner[0])


def create_i18n_middleware(config: AppConfig) -> I18nMiddleware:
    loader = FluentResourceLoader(roots=f"{LOCALES_DIR}/{{locale}}")
    locales = {
        locale: FluentLocalization(
            locales=[locale, config.i18n.default_locale],
            resource_ids=RESOURCE_I18N,
            resource_loader=loader,
        )
        for locale in config.i18n.locales
    }
    return I18nMiddleware(locales=locales, default_locale=config.i18n.default_locale)


def create_middlewares(config: AppConfig) -> Middlewares:
    i18n_middleware = create_i18n_middleware(config)
    error_middleware = ErrorMiddleware()
    user_middleware = UserMiddleware()
    throttling_middleware = ThrottlingMiddleware()
    maintenance_middleware = MaintenanceMiddleware()
    garbage_middleware = GarbageMiddleware()
    # TODO: Implement middleware for global user lookup
    # TODO: Implement middleware for action auditing

    # NOTE: Order matters!
    outer_middlewares = [
        error_middleware,
        user_middleware,
        throttling_middleware,
        maintenance_middleware,
    ]
    inner_middlewares = [
        i18n_middleware,
        garbage_middleware,
    ]

    return Middlewares(outer=outer_middlewares, inner=inner_middlewares)
