from contextlib import asynccontextmanager
from typing import AsyncGenerator

from aiogram import Bot
from fastapi import FastAPI
from loguru import logger

from app.core.container import AppContainer
from app.core.enums import SystemNotificationType
from app.endpoints.telegram import TelegramRequestHandler


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    bot: Bot = app.state.bot
    container: AppContainer = app.state.container
    handler: TelegramRequestHandler = app.state.tg_webhook_handler

    bot_info = await bot.get_me()
    states: dict[bool | None, str] = {True: "Enabled", False: "Disabled", None: "Unknown"}

    logger.info("Bot settings:")
    logger.info("-----------------------")
    logger.info(f"Groups Mode  - {states[bot_info.can_join_groups]}")
    logger.info(f"Privacy Mode - {states[not bot_info.can_read_all_group_messages]}")
    logger.info(f"Inline Mode  - {states[bot_info.supports_inline_queries]}")
    logger.info("-----------------------")

    await handler.startup()
    logger.info("Bot started successfully")

    maintenance_mode = await container.services.maintenance.get_current_mode()
    logger.warning(f"Bot in maintenance mode: '{maintenance_mode}'")

    await container.services.notification.system_notify(
        devs=await container.services.user.get_devs(),
        ntf_type=SystemNotificationType.BOT_LIFETIME,
        text_key="ntf-event-bot-startup",
        mode=maintenance_mode,
    )

    yield

    await container.services.notification.system_notify(
        devs=await container.services.user.get_devs(),
        ntf_type=SystemNotificationType.BOT_LIFETIME,
        text_key="ntf-event-bot-shutdown",
    )

    await handler.shutdown()
    logger.info("Bot stopped")
