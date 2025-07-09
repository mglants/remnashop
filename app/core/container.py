from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from redis.asyncio import Redis
    from remnawave_api import RemnawaveSDK
    from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

    from app.bot.middlewares import I18nMiddleware
    from app.bot.services import (
        MaintenanceService,
        NotificationService,
        PlanService,
        UserService,
    )
    from app.db.repositories import RedisRepository

    from .config import AppConfig

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class ServiceContainer:
    user: UserService
    plan: PlanService
    # promocode: PromocodeService

    maintenance: MaintenanceService
    notification: NotificationService


@dataclass(frozen=True, slots=True)
class AppContainer:
    config: AppConfig
    i18n: I18nMiddleware
    session_pool: async_sessionmaker[AsyncSession]
    redis: Redis
    remnawave: RemnawaveSDK

    redis_repository: RedisRepository

    services: ServiceContainer
