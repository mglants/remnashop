from typing import Final

from aiogram import Router
from aiogram.filters import JOIN_TRANSITION, LEAVE_TRANSITION, ChatMemberUpdatedFilter
from aiogram.types import ChatMemberUpdated
from loguru import logger

from app.core.container import AppContainer
from app.db.models.dto import UserDto

router: Final[Router] = Router(name=__name__)
# NOTE: For only ChatType.PRIVATE (app/bot/filters/private.py)


@router.my_chat_member(ChatMemberUpdatedFilter(JOIN_TRANSITION))
async def bot_unblocked(_: ChatMemberUpdated, user: UserDto, container: AppContainer) -> None:
    logger.info("unblock")
    # TODO: unblock


@router.my_chat_member(ChatMemberUpdatedFilter(LEAVE_TRANSITION))
async def bot_blocked(_: ChatMemberUpdated, user: UserDto, container: AppContainer) -> None:
    logger.info("block")
    # TODO: block
