from aiogram import Dispatcher
from aiogram.filters import ExceptionTypeFilter
from aiogram.fsm.storage.base import DefaultKeyBuilder
from aiogram.fsm.storage.redis import RedisStorage
from aiogram_dialog import setup_dialogs
from aiogram_dialog.api.exceptions import UnknownIntent, UnknownState

from app.bot.commands import commands_delete, commands_setup
from app.bot.filters import PrivateFilter
from app.bot.routers import routers
from app.bot.routers.extra.errors import on_unknown_intent, on_unknown_state
from app.bot.webhook import webhook_shutdown, webhook_startup
from app.core.container import AppContainer
from app.core.utils import mjson
from app.factories.middlewares import Middlewares


def create_dispatcher(container: AppContainer, middlewares: Middlewares) -> Dispatcher:
    dispatcher = Dispatcher(
        storage=RedisStorage(
            redis=container.redis,
            key_builder=DefaultKeyBuilder(with_destiny=True),
            json_loads=mjson.decode,
            json_dumps=mjson.encode,
        ),
        container=container,
    )

    # request -> outer -> filter -> inner -> handler #
    setup_dialogs(router=dispatcher)

    for mw in middlewares.outer:
        mw.setup_outer(router=dispatcher)

    for mw in middlewares.inner:
        mw.setup_inner(router=dispatcher)

    dispatcher.errors.register(on_unknown_intent, ExceptionTypeFilter(UnknownIntent))
    dispatcher.errors.register(on_unknown_state, ExceptionTypeFilter(UnknownState))

    dispatcher.startup.register(webhook_startup)
    dispatcher.startup.register(commands_setup)

    dispatcher.shutdown.register(webhook_shutdown)
    dispatcher.shutdown.register(commands_delete)

    dispatcher.message.filter(PrivateFilter())  # global filter allows only private chats
    dispatcher.include_routers(*routers)
    return dispatcher
