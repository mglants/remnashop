from typing import Any

from aiogram import Bot
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
from app.core.config import AppConfig
from app.core.container import AppContainer, ServiceContainer
from app.db.repositories import RedisRepository


def create_container(
    bot: Bot,
    config: AppConfig,
    redis: Redis,
    session_pool: async_sessionmaker[AsyncSession],
    i18n: I18nMiddleware,
    remnawave: RemnawaveSDK,
) -> AppContainer:
    redis_repository = RedisRepository(client=redis, config=config)

    service_kwargs: dict[str, Any] = {
        "bot": bot,
        "config": config,
        "redis": redis,
        "redis_repository": redis_repository,
        "session_pool": session_pool,
        "i18n": i18n,
    }

    user_service = UserService(**service_kwargs)
    plan_service = PlanService(**service_kwargs)

    maintenance_service = MaintenanceService(**service_kwargs)
    notification_service = NotificationService(**service_kwargs)

    services = ServiceContainer(
        user=user_service,
        plan=plan_service,
        maintenance=maintenance_service,
        notification=notification_service,
    )

    return AppContainer(
        config=config,
        session_pool=session_pool,
        redis=redis,
        i18n=i18n,
        remnawave=remnawave,
        redis_repository=redis_repository,
        services=services,
    )
