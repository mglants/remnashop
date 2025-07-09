from typing import Final

from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram_dialog import DialogManager, ShowMode, StartMode
from loguru import logger

from app.bot.states import MainMenu
from app.core.utils.formatters import format_log_user
from app.db.models.dto import UserDto

router: Final[Router] = Router(name=__name__)


@router.message(CommandStart())
async def on_start_command(
    message: Message,
    user: UserDto,
    dialog_manager: DialogManager,
) -> None:
    logger.info(f"{format_log_user(user)} Started dialog")
    await dialog_manager.start(
        state=MainMenu.MAIN,
        mode=StartMode.RESET_STACK,
        show_mode=ShowMode.DELETE_AND_SEND,
    )
