from typing import Final

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram_dialog.api.exceptions import UnknownIntent, UnknownState
from loguru import logger

from app.core.utils.formatters import format_log_user
from app.db.models.dto import UserDto

router: Final[Router] = Router(name=__name__)


@router.message(Command("test"))
async def on_test_command(message: Message, user: UserDto) -> None:
    logger.info(f"{format_log_user(user)} Test command executed")
    raise UnknownState("test_state")
