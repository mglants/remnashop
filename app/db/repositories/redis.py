from typing import Any, Awaitable, Final, Optional, Set, TypeVar, cast

from pydantic import BaseModel, TypeAdapter
from redis.asyncio import Redis
from redis.typing import ExpiryT

from app.core.config import AppConfig
from app.core.storage_keys import (
    SystemNotificationSettingsKey,
    UserNotificationSettingsKey,
    WebhookLockKey,
)
from app.core.utils import mjson
from app.core.utils.key_builder import StorageKey
from app.db.models.dto import SystemNotificationDto, UserNotificationDto

T = TypeVar("T", bound=Any)

TX_QUEUE_KEY: Final[str] = "tx_queue"


class RedisRepository:
    client: Redis
    config: AppConfig

    def __init__(self, client: Redis, config: AppConfig) -> None:
        self.client = client
        self.config = config

    async def get(
        self,
        key: StorageKey,
        validator: type[T],
        default: Optional[T] = None,
    ) -> Optional[T]:
        value: Optional[Any] = await self.client.get(key.pack())
        if value is None:
            return default
        value = mjson.decode(value)
        return TypeAdapter[T](validator).validate_python(value)

    async def set(self, key: StorageKey, value: Any, ex: Optional[ExpiryT] = None) -> None:
        if isinstance(value, BaseModel):
            value = value.model_dump(exclude_defaults=True)
        await self.client.set(name=key.pack(), value=mjson.encode(value), ex=ex)

    async def exists(self, key: StorageKey) -> bool:
        return cast(bool, await self.client.exists(key.pack()))

    async def delete(self, key: StorageKey) -> None:
        await self.client.delete(key.pack())

    async def close(self) -> None:
        await self.client.aclose(close_connection_pool=True)

    async def collection_add(self, key: StorageKey, *values: Any) -> int:
        str_values = [str(v) for v in values]
        return await cast(Awaitable[int], self.client.sadd(key.pack(), *str_values))

    async def collection_members(self, key: StorageKey) -> list[str]:
        members_bytes = await cast(Awaitable[Set[bytes]], self.client.smembers(key.pack()))
        return [member.decode() for member in members_bytes]

    async def collection_is_member(self, key: StorageKey, value: Any) -> bool:
        return await cast(Awaitable[bool], self.client.sismember(key.pack(), str(value)))

    async def collection_remove(self, key: StorageKey, *values: Any) -> int:
        str_values = [str(v) for v in values]
        return await cast(Awaitable[int], self.client.srem(key.pack(), *str_values))

    async def is_webhook_set(self, bot_id: int, webhook_hash: str) -> bool:
        key: WebhookLockKey = WebhookLockKey(
            bot_id=bot_id,
            webhook_hash=webhook_hash,
        )
        return await self.exists(key=key)

    async def set_webhook(self, bot_id: int, webhook_hash: str) -> None:
        key: WebhookLockKey = WebhookLockKey(
            bot_id=bot_id,
            webhook_hash=webhook_hash,
        )
        await self.set(key=key, value=None)

    async def clear_webhooks(self, bot_id: int) -> None:
        key: WebhookLockKey = WebhookLockKey(bot_id=bot_id, webhook_hash="*")
        keys: list[bytes] = await self.client.keys(key.pack())
        if not keys:
            return
        await self.client.delete(*keys)

    async def get_system_notification_settings(self) -> SystemNotificationDto:
        key = SystemNotificationSettingsKey()
        settings = await self.get(
            key=key, validator=SystemNotificationDto, default=SystemNotificationDto()
        )
        return cast(SystemNotificationDto, settings)

    async def set_system_notification_settings(self, data: SystemNotificationDto) -> None:
        key = SystemNotificationSettingsKey()
        await self.set(key=key, value=data)

    async def get_user_notification_settings(self) -> UserNotificationDto:
        key = UserNotificationSettingsKey()
        settings = await self.get(
            key=key, validator=UserNotificationDto, default=UserNotificationDto()
        )
        return cast(UserNotificationDto, settings)

    async def set_user_notification_settings(self, data: UserNotificationDto) -> None:
        key = UserNotificationSettingsKey()
        await self.set(key=key, value=data)
