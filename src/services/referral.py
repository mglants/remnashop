from typing import List, Optional

from aiogram import Bot
from fluentogram import TranslatorHub
from loguru import logger
from redis.asyncio import Redis

from src.core.config import AppConfig
from src.core.constants import REFERRAL_PREFIX
from src.core.enums import ReferralLevel, ReferralRewardType
from src.infrastructure.database import UnitOfWork
from src.infrastructure.database.models.dto import ReferralDto, ReferralRewardDto, UserDto
from src.infrastructure.database.models.sql import Referral, ReferralReward
from src.infrastructure.redis import RedisRepository
from src.services.user import UserService

from .base import BaseService


class ReferralService(BaseService):
    uow: UnitOfWork
    user_service: UserService
    _bot_username: Optional[str]

    def __init__(
        self,
        config: AppConfig,
        bot: Bot,
        redis_client: Redis,
        redis_repository: RedisRepository,
        translator_hub: TranslatorHub,
        #
        uow: UnitOfWork,
        user_service: UserService,
    ) -> None:
        super().__init__(config, bot, redis_client, redis_repository, translator_hub)
        self.uow = uow
        self.user_service = user_service
        self._bot_username: Optional[str] = None

    async def create_referral(
        self,
        referrer: UserDto,
        referred: UserDto,
        level: ReferralLevel,
    ) -> ReferralDto:
        referral = await self.uow.repository.referrals.create_referral(
            Referral(
                referrer_telegram_id=referrer.telegram_id,
                referred_telegram_id=referred.telegram_id,
                level=level,
            )
        )
        logger.info(f"Referral created: {referrer.telegram_id} -> {referred.telegram_id}")
        return ReferralDto.from_model(referral)  # type: ignore[return-value]

    async def get_referral_by_referred(self, telegram_id: int) -> Optional[ReferralDto]:
        referral = await self.uow.repository.referrals.get_referral_by_referred(telegram_id)
        return ReferralDto.from_model(referral) if referral else None

    async def get_referrals_by_referrer(self, telegram_id: int) -> List[ReferralDto]:
        referrals = await self.uow.repository.referrals.get_referrals_by_referrer(telegram_id)
        return ReferralDto.from_model_list(referrals)

    async def create_reward(
        self,
        referral_id: int,
        user_telegram_id: int,
        reward_type: ReferralRewardType,
        reward_amount: int,
    ) -> ReferralRewardDto:
        reward = await self.uow.repository.referrals.create_reward(
            ReferralReward(
                referral_id=referral_id,
                user_telegram_id=user_telegram_id,
                reward_type=reward_type,
                reward_amount=reward_amount,
            )
        )
        logger.info(f"ReferralReward created: referral={referral_id}, user={user_telegram_id}")
        return ReferralRewardDto.from_model(reward)  # type: ignore[return-value]

    async def get_rewards_by_user(self, telegram_id: int) -> List[ReferralRewardDto]:
        rewards = await self.uow.repository.referrals.get_rewards_by_user(telegram_id)
        return ReferralRewardDto.from_model_list(rewards)

    async def get_rewards_by_referral(self, referral_id: int) -> List[ReferralRewardDto]:
        rewards = await self.uow.repository.referrals.get_rewards_by_referral(referral_id)
        return ReferralRewardDto.from_model_list(rewards)

    #

    async def handle_referral(self, user: UserDto, code: str) -> None:
        referrer = await self.user_service.get_by_referral_code(code)
        if not referrer:
            logger.warning("")
            return

        if not referrer or referrer.telegram_id == user.telegram_id:
            logger.warning("")
            return

        parent = await self.get_referral_by_referred(referrer.telegram_id)

        if parent:
            level = ReferralLevel.SECOND
        else:
            level = ReferralLevel.FIRST

        await self.create_referral(
            referrer=referrer,
            referred=user,
            level=level,
        )

    async def get_ref_link(self, referral_code: str) -> str:
        return f"{await self._get_bot_redirect_url()}={REFERRAL_PREFIX}{referral_code}"

    async def _get_bot_redirect_url(self) -> str:
        if self._bot_username is None:
            self._bot_username = (await self.bot.get_me()).username
        return f"https://t.me/{self._bot_username}"
