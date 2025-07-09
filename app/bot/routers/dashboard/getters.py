from typing import Any

from aiogram_dialog import DialogManager

from app.core.container import AppContainer


async def maintenance_getter(
    dialog_manager: DialogManager,
    container: AppContainer,
    **kwargs: Any,
) -> dict[str, Any]:
    current_mode = await container.services.maintenance.get_current_mode()
    modes = await container.services.maintenance.get_available_modes()

    return {
        "status": current_mode,
        "modes": modes,
    }
