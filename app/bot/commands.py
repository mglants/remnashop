from typing import Optional

from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeAllPrivateChats
from loguru import logger

from app.core.container import AppContainer
from app.core.enums import Command, Locale


async def commands_setup(bot: Bot, container: AppContainer) -> None:
    if not container.config.bot.setup_commands:
        logger.debug("Bot commands setup is disabled")
        return

    locales_to_set: list[Optional[Locale]] = list(container.config.i18n.locales) + [None]

    for lang_code in locales_to_set:
        display_lang_code = lang_code if lang_code else "default"
        formatter = container.i18n.get_formatter(
            locale=lang_code or container.config.i18n.default_locale
        )

        commands_for_locale = [
            BotCommand(
                command=cmd_enum.value.command,
                description=formatter(cmd_enum.value.description, {}),
            )
            for cmd_enum in Command
        ]

        success = await bot.set_my_commands(
            commands=commands_for_locale,
            scope=BotCommandScopeAllPrivateChats(),
            language_code=lang_code,
        )

        if success:
            logger.info(
                f"Commands successfully set for language '{display_lang_code}': "
                f"{[cmd.command for cmd in commands_for_locale]}"
            )
        else:
            logger.error(f"Failed to set commands for language '{display_lang_code}'")


async def commands_delete(bot: Bot, container: AppContainer) -> None:
    if not container.config.bot.setup_commands:
        logger.debug("Bot commands deletion is disabled")
        return

    locales_to_delete: list[Optional[str]] = list(container.config.i18n.locales) + [None]

    for lang_code in locales_to_delete:
        display_lang_code = lang_code if lang_code else "default"

        success = await bot.delete_my_commands(
            scope=BotCommandScopeAllPrivateChats(),
            language_code=lang_code,
        )

        if success:
            logger.info(f"Commands deleted for '{display_lang_code}'")
        else:
            logger.error(f"Failed to delete commands for '{display_lang_code}'")
