from typing import Optional

from aiogram.types import User as AiogramUser
from loguru import logger

from app.core.cache_wrapper import redis_cache
from app.core.constants import TIME_1M, TIME_10M
from app.core.enums import UserRole
from app.core.utils.key_builder import build_key
from app.db.models.dto import UserDto
from app.db.models.sql import User
from app.db.uow import UnitOfWork

from .base import BaseService


class UserService(BaseService):
    async def clear_cache(self, user_id: Optional[int] = None) -> None:
        keys_to_delete: list[str] = []

        # Invalidate specific user cache
        if user_id is not None:
            user_cache_key: str = build_key("cache", "get_user", user_id=user_id)
            keys_to_delete.append(user_cache_key)
            logger.info(f"Adding user_id {user_id} to cache invalidation list.")

        # Invalidate all relevant list caches
        list_cache_keys_to_invalidate = [
            build_key("cache", "get_by_role", role=UserRole.DEV.value),
            build_key("cache", "get_by_role", role=UserRole.ADMIN.value),
            build_key("cache", "get_by_role", role=UserRole.USER.value),
            build_key("cache", "get_devs"),
            build_key("cache", "get_admins"),
            build_key("cache", "get_blocked_users"),
            build_key("cache", "count"),
        ]
        keys_to_delete.extend(list_cache_keys_to_invalidate)
        logger.info(f"Adding {len(list_cache_keys_to_invalidate)} list keys to cache invalidation.")

        if keys_to_delete:
            await self.redis.delete(*keys_to_delete)
            logger.info(f"Total {len(keys_to_delete)} cache keys invalidated in one operation.")
        else:
            logger.info("No cache keys to invalidate.")

    async def create(self, aiogram_user: AiogramUser) -> UserDto:
        async with UnitOfWork(self.session_pool) as uow:
            db_user = User(
                telegram_id=aiogram_user.id,
                name=aiogram_user.full_name,
                role=(UserRole.DEV if self.config.bot.dev_id == aiogram_user.id else UserRole.USER),
                language=(
                    aiogram_user.language_code
                    if aiogram_user.language_code in self.i18n.locales
                    else self.i18n.default_locale
                ),
            )
            uow.repository.add(db_user)
        await self.clear_cache(user_id=aiogram_user.id)
        return db_user.dto()

    @redis_cache(prefix="get_user", ttl=TIME_1M)
    async def get(self, telegram_id: int) -> Optional[UserDto]:
        async with UnitOfWork(self.session_pool) as uow:
            db_user = await uow.repository.users.get(telegram_id=telegram_id)
            return db_user.dto() if db_user else None

    async def update(self, user: UserDto) -> Optional[UserDto]:
        async with UnitOfWork(self.session_pool) as uow:
            db_user = await uow.repository.users.get(telegram_id=user.telegram_id)

            if not db_user:
                return None

            db_user = await uow.repository.users.update(
                user.telegram_id,
                **user.model_state,
            )
        if db_user:
            await self.clear_cache(user_id=user.telegram_id)
        return db_user.dto() if db_user else None

    async def delete(self, user: UserDto) -> bool:
        async with UnitOfWork(self.session_pool) as uow:
            result = await uow.repository.users.delete(telegram_id=user.telegram_id)
        if result:
            await self.clear_cache(user_id=user.telegram_id)
        return result

    @redis_cache(prefix="count", ttl=TIME_1M)
    async def count(self) -> int:
        async with UnitOfWork(self.session_pool) as uow:
            return await uow.repository.users.count()

    @redis_cache(prefix="get_by_role", ttl=TIME_1M)
    async def get_by_role(self, role: UserRole) -> list[UserDto]:
        async with UnitOfWork(self.session_pool) as uow:
            users = await uow.repository.users.filter_by_role(role)
            return [user.dto() for user in users]

    @redis_cache(prefix="get_devs", ttl=TIME_10M)
    async def get_devs(self) -> list[UserDto]:
        async with UnitOfWork(self.session_pool) as uow:
            devs = await uow.repository.users.filter_by_role(UserRole.DEV)
            return [dev.dto() for dev in devs]

    @redis_cache(prefix="get_admins", ttl=TIME_10M)
    async def get_admins(self) -> list[UserDto]:
        async with UnitOfWork(self.session_pool) as uow:
            admins = await uow.repository.users.filter_by_role(UserRole.ADMIN)
            return [admin.dto() for admin in admins]

    @redis_cache(prefix="get_admins", ttl=TIME_10M)
    async def get_blocked_users(self) -> list[UserDto]:
        async with UnitOfWork(self.session_pool) as uow:
            users = await uow.repository.users.filter_by_blocked()
            return [user.dto() for user in users]

    async def set_block(self, user: UserDto, blocked: bool) -> None:
        user.is_blocked = blocked
        async with UnitOfWork(self.session_pool) as uow:
            await uow.repository.users.update(
                telegram_id=user.telegram_id,
                **user.model_state,
            )
        await self.clear_cache(user_id=user.telegram_id)

    async def set_bot_blocked(self, user: UserDto, blocked: bool) -> None:
        user.is_bot_blocked = blocked
        async with UnitOfWork(self.session_pool) as uow:
            await uow.repository.users.update(
                telegram_id=user.telegram_id,
                **user.model_state,
            )
        await self.clear_cache(user_id=user.telegram_id)

    async def set_role(self, user: UserDto, role: UserRole) -> None:
        user.role = role
        async with UnitOfWork(self.session_pool) as uow:
            await uow.repository.users.update(
                telegram_id=user.telegram_id,
                **user.model_state,
            )
        await self.clear_cache(user_id=user.telegram_id)
