from aiogram import Bot
from loguru import logger
from redis.asyncio import Redis
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.bot.middlewares import I18nMiddleware
from app.core.config import AppConfig
from app.db.repositories import RedisRepository


class BaseService:
    bot: Bot
    config: AppConfig
    redis: Redis
    redis_repository: RedisRepository
    session_pool: async_sessionmaker[AsyncSession]
    i18n: I18nMiddleware

    def __init__(
        self,
        bot: Bot,
        config: AppConfig,
        redis: Redis,
        redis_repository: RedisRepository,
        session_pool: async_sessionmaker[AsyncSession],
        i18n: I18nMiddleware,
    ) -> None:
        logger.debug(f"{self.__class__.__name__} initialized")

        self.bot = bot
        self.config = config
        self.redis = redis
        self.redis_repository = redis_repository
        self.session_pool = session_pool
        self.i18n = i18n
        self.i18n = i18n
