from dishka.integrations.taskiq import FromDishka, inject
from loguru import logger

from src.core.enums import ReferralRewardType
from src.infrastructure.database.models.dto.user import UserDto
from src.infrastructure.taskiq.broker import broker
from src.services.referral import ReferralService


@broker.task
@inject
async def assign_referral_reward_task(
    user: UserDto,
    referral_service: FromDishka[ReferralService],
) -> None:
    logger.info(f"")

    referral = await referral_service.get_referral_by_referred(user.telegram_id)

    if not referral:
        return

    await referral_service.create_reward(
        referral_id=referral.id,  # type: ignore[arg-type]
        user_telegram_id=user.telegram_id,
        reward_type=ReferralRewardType.POINTS,
        reward_amount=100,
    )

    parent = await referral_service.get_referral_by_referred(referral.referrer.telegram_id)

    if parent:
        await referral_service.create_reward(
            referral_id=referral.id,  # type: ignore[arg-type]
            user_telegram_id=user.telegram_id,
            reward_type=ReferralRewardType.POINTS,
            reward_amount=100,
        )


@broker.task(schedule=[{"cron": "*/15 * * * *"}])
@inject
async def distribute_referral_rewards_task() -> None:
    NotImplemented
