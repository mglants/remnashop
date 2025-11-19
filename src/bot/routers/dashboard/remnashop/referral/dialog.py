from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Button, Column, Row, Select, Start, SwitchTo
from magic_filter import F

from src.bot.keyboards import main_menu_button
from src.bot.routers.dashboard.remnashop.referral.getters import (
    accrual_strategy_getter,
    level_getter,
    referral_getter,
    reward_getter,
    reward_strategy_getter,
)
from src.bot.routers.dashboard.remnashop.referral.handlers import (
    on_accrual_strategy_select,
    on_enable_toggle,
    on_level_select,
    on_reward_select,
    on_reward_strategy_select,
)
from src.bot.states import DashboardRemnashop, RemnashopReferral
from src.bot.widgets import Banner, I18nFormat, IgnoreUpdate
from src.core.enums import (
    BannerName,
    ReferralAccrualStrategy,
    ReferralLevel,
    ReferralRewardStrategy,
    ReferralRewardType,
)

referral = Window(
    Banner(BannerName.DASHBOARD),
    I18nFormat("msg-referral-main"),
    Row(
        Button(
            text=I18nFormat("btn-referral-enable"),
            id="enable",
            on_click=on_enable_toggle,
        ),
    ),
    Row(
        SwitchTo(
            text=I18nFormat("btn-referral-level"),
            id="level",
            state=RemnashopReferral.LEVEL,
        ),
        SwitchTo(
            text=I18nFormat("btn-referral-reward"),
            id="reward",
            state=RemnashopReferral.REWARD,
        ),
    ),
    Row(
        SwitchTo(
            text=I18nFormat("btn-referral-accrual-strategy"),
            id="strategy",
            state=RemnashopReferral.ACCRUAL_STRATEGY,
        ),
    ),
    Row(
        SwitchTo(
            text=I18nFormat("btn-referral-reward-strategy"),
            id="strategy",
            state=RemnashopReferral.REWARD_STRATEGY,
        ),
    ),
    Row(
        Start(
            text=I18nFormat("btn-back"),
            id="back",
            state=DashboardRemnashop.MAIN,
        ),
        *main_menu_button,
    ),
    IgnoreUpdate(),
    state=RemnashopReferral.MAIN,
    getter=referral_getter,
)

level = Window(
    Banner(BannerName.DASHBOARD),
    I18nFormat("msg-referral-level"),
    Row(
        Select(
            text=I18nFormat("btn-referral-level-choice", type=F["item"]),
            id="select_level",
            item_id_getter=lambda item: item.value,
            items="levels",
            type_factory=ReferralLevel,
            on_click=on_level_select,
        ),
    ),
    Row(
        SwitchTo(
            text=I18nFormat("btn-back"),
            id="back",
            state=RemnashopReferral.MAIN,
        ),
    ),
    IgnoreUpdate(),
    state=RemnashopReferral.LEVEL,
    getter=level_getter,
)

reward = Window(
    Banner(BannerName.DASHBOARD),
    I18nFormat("msg-referral-reward"),
    Column(
        Select(
            text=I18nFormat("btn-referral-reward-choice", type=F["item"]),
            id="select_reward",
            item_id_getter=lambda item: item.value,
            items="rewards",
            type_factory=ReferralRewardType,
            on_click=on_reward_select,
        ),
    ),
    Row(
        SwitchTo(
            text=I18nFormat("btn-back"),
            id="back",
            state=RemnashopReferral.MAIN,
        ),
    ),
    IgnoreUpdate(),
    state=RemnashopReferral.REWARD,
    getter=reward_getter,
)

accrual_strategy = Window(
    Banner(BannerName.DASHBOARD),
    I18nFormat("msg-referral-accrual-strategy"),
    Column(
        Select(
            text=I18nFormat("btn-referral-accrual-strategy-choice", type=F["item"]),
            id="select_strategy",
            item_id_getter=lambda item: item.value,
            items="strategys",
            type_factory=ReferralAccrualStrategy,
            on_click=on_accrual_strategy_select,
        ),
    ),
    Row(
        SwitchTo(
            text=I18nFormat("btn-back"),
            id="back",
            state=RemnashopReferral.MAIN,
        ),
    ),
    IgnoreUpdate(),
    state=RemnashopReferral.ACCRUAL_STRATEGY,
    getter=accrual_strategy_getter,
)

reward_strategy = Window(
    Banner(BannerName.DASHBOARD),
    I18nFormat("msg-referral-reward-strategy"),
    Column(
        Select(
            text=I18nFormat("btn-referral-reward-strategy-choice", type=F["item"]),
            id="select_strategy",
            item_id_getter=lambda item: item.value,
            items="strategys",
            type_factory=ReferralRewardStrategy,
            on_click=on_reward_strategy_select,
        ),
    ),
    Row(
        SwitchTo(
            text=I18nFormat("btn-back"),
            id="back",
            state=RemnashopReferral.MAIN,
        ),
    ),
    IgnoreUpdate(),
    state=RemnashopReferral.REWARD_STRATEGY,
    getter=reward_strategy_getter,
)

router = Dialog(
    referral,
    level,
    reward,
    accrual_strategy,
    reward_strategy,
)
