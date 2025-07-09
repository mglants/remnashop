from typing import Final

from aiogram_dialog import Dialog, StartMode, Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button, Row, Start

from app.bot.conditions import is_privileged
from app.bot.routers.dashboard.users.handlers import on_user_search
from app.bot.states import Dashboard, MainMenu
from app.bot.widgets import Banner, I18nFormat, IgnoreUpdate
from app.core.enums import BannerName

from .getters import menu_getter

menu = Window(
    Banner(BannerName.MENU),
    I18nFormat("msg-menu-profile"),
    I18nFormat("separator"),
    I18nFormat("msg-menu-subscription"),
    # Row(
    #     Button(
    #         text=I18nFormat(ButtonKey.CONNECT),
    #         id="connect",
    #     ),
    # ),
    # Row(
    #     Button(
    #         text=I18nFormat(ButtonKey.TRIAL),
    #         id="trial",
    #     ),
    # ),
    Row(
        # Button(
        #     text=I18nFormat(ButtonKey.PROMOCODE),
        #     id="promocode",
        # ),
        Button(
            text=I18nFormat("btn-menu-subscription"),
            id="subscription",
        ),
    ),
    Row(
        Button(
            text=I18nFormat("btn-menu-invite"),
            id="invite",
        ),
        Button(
            text=I18nFormat("btn-menu-support"),
            id="support",
        ),
    ),
    Row(
        Start(
            text=I18nFormat("btn-menu-dashboard"),
            id="dashboard",
            state=Dashboard.MAIN,
            mode=StartMode.RESET_STACK,
            when=is_privileged,
        ),
    ),
    MessageInput(func=on_user_search),
    IgnoreUpdate(),
    state=MainMenu.MAIN,
    getter=menu_getter,
)

router: Final[Dialog] = Dialog(
    menu,
)
