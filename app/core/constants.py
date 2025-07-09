from datetime import timezone
from pathlib import Path
from typing import Final

BASE_DIR: Final[Path] = Path(__file__).resolve().parents[2]
ASSETS_DIR: Final[Path] = BASE_DIR / "app" / "assets"
BANNERS_DIR: Final[Path] = ASSETS_DIR / "banners"
LOCALES_DIR: Final[Path] = ASSETS_DIR / "locales"
LOG_DIR: Final[Path] = BASE_DIR / "logs"

DOMAIN_REGEX: Final[str] = r"^(?:[a-zA-Z0-9-]+\.)+[a-zA-Z]{2,}$"
API_V1: Final[str] = "/api/v1"
WEBHOOK_PATH: Final[str] = "/telegram"

TIMEZONE: Final[timezone] = timezone.utc
UNLIMITED: Final[str] = "∞"

# Resource file names for i18n
RESOURCE_I18N: Final[list[str]] = [
    "messages.ftl",
    "buttons.ftl",
    "notifications.ftl",
    "utils.ftl",
]

# Keys for data
DIALOG_MANAGER_KEY: Final[str] = "dialog_manager"
MIDDLEWARE_DATA_KEY: Final[str] = "middleware_data"
APP_CONTAINER_KEY: Final[str] = "container"
BOT_KEY: Final[str] = "bot"
USER_KEY: Final[str] = "user"
I18N_FORMATTER_KEY: Final[str] = "i18n_formatter"

# Time constants
TIME_1M: Final[int] = 60
TIME_5M: Final[int] = TIME_1M * 5
TIME_10M: Final[int] = TIME_1M * 10
