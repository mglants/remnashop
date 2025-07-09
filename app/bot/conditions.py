from typing import Any

from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.common import Whenable

from app.core.constants import APP_CONTAINER_KEY, USER_KEY
from app.core.container import AppContainer
from app.db.models.dto import UserDto


def is_admin(data: dict[str, Any], widget: Whenable, dialog_manager: DialogManager) -> bool:
    user: UserDto = dialog_manager.middleware_data[USER_KEY]
    return user.is_admin


def is_dev(data: dict[str, Any], widget: Whenable, dialog_manager: DialogManager) -> bool:
    user: UserDto = dialog_manager.middleware_data[USER_KEY]
    return user.is_dev


def is_privileged(data: dict[str, Any], widget: Whenable, dialog_manager: DialogManager) -> bool:
    user: UserDto = dialog_manager.middleware_data[USER_KEY]
    return user.is_admin or user.is_dev


def is_super_dev(data: dict[str, Any], widget: Whenable, dialog_manager: DialogManager) -> bool:
    user: UserDto = dialog_manager.middleware_data[USER_KEY]
    container: AppContainer = dialog_manager.middleware_data[APP_CONTAINER_KEY]
    return user.telegram_id == container.config.bot.dev_id
