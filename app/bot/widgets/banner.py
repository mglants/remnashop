import functools
from pathlib import Path
from typing import Any, Optional, Tuple

from aiogram.types import ContentType
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.common import Whenable
from aiogram_dialog.widgets.media import StaticMedia
from loguru import logger

from app.core.constants import APP_CONTAINER_KEY, BANNERS_DIR
from app.core.container import AppContainer
from app.core.enums import BannerFormat, BannerName


@functools.lru_cache(maxsize=None)
def get_banner_path_and_type(name: BannerName) -> Tuple[Path, ContentType]:
    path: Optional[Path]
    content_type: Optional[ContentType]

    for fmt in BannerFormat:
        candidate_path = BANNERS_DIR / f"{name.value}.{fmt.value}"
        if candidate_path.exists():
            path = candidate_path
            content_type = fmt.content_type
            logger.debug(
                f"Determined banner path for '{name.value}': '{path}' with type '{content_type}'"
            )
            break
    else:
        logger.warning(f"Banner file for '{name.value}' not found, using default banner")
        path = BANNERS_DIR / f"{BannerName.DEFAULT.value}.{BannerFormat.JPG.value}"
        content_type = BannerFormat.JPG.content_type

    if not path.exists():
        raise FileNotFoundError(f"Default banner file not found: '{path}' at '{BANNERS_DIR}'")

    return path, content_type


class Banner(StaticMedia):
    def __init__(self, name: BannerName) -> None:
        path, content_type = get_banner_path_and_type(name)

        def is_use_banners(
            data: dict[str, Any],
            widget: Whenable,
            dialog_manager: DialogManager,
        ) -> bool:
            container: AppContainer = dialog_manager.middleware_data[APP_CONTAINER_KEY]
            return container.config.bot.use_banners

        super().__init__(path=path, type=content_type, when=is_use_banners)
