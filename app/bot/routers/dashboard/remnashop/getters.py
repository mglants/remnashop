from typing import Any

from aiogram_dialog import DialogManager

from app.core.container import AppContainer
from app.db.models.dto import UserDto


async def admins_getter(
    dialog_manager: DialogManager,
    container: AppContainer,
    **kwargs: Any,
) -> dict[str, Any]:
    devs: list[UserDto] = await container.services.user.get_devs()
    admins: list[UserDto] = await container.services.user.get_admins()

    return {"admins": devs + admins}
