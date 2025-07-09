from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, StartMode
from aiogram_dialog.widgets.kbd import Button
from loguru import logger

from app.bot.states import DashboardRemnawave
from app.core.constants import APP_CONTAINER_KEY, USER_KEY
from app.core.container import AppContainer
from app.db.models.dto import UserDto


async def start_remnawave_window(
    callback: CallbackQuery,
    widget: Button,
    dialog_manager: DialogManager,
) -> None:
    user: UserDto = dialog_manager.middleware_data[USER_KEY]
    container: AppContainer = dialog_manager.middleware_data[APP_CONTAINER_KEY]

    try:
        response = await container.remnawave.system.get_stats()
    except Exception as exception:
        logger.error(f"Remnawave: {exception}")
        await container.services.notification.notify_user(
            user=user,
            text_key="ntf-error-connect-remnawave",
        )
        return

    await dialog_manager.start(state=DashboardRemnawave.MAIN, mode=StartMode.RESET_STACK)
