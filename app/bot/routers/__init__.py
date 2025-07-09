from . import dashboard, extra, menu
from .dashboard import broadcast, promocodes, remnashop, remnawave, users

# NOTE: Order matters!
routers = [
    extra.notification.router,  # NOTE: Must be registered first to handle notifications!
    #
    menu.handlers.router,  # NOTE: Must be registered second to handle common entrypoints!
    menu.dialog.router,
    #
    dashboard.dialog.router,
    broadcast.dialog.router,
    promocodes.dialog.router,
    #
    remnashop.dialog.router,
    remnashop.notifications.dialog.router,
    remnashop.plans.dialog.router,
    #
    remnawave.dialog.router,
    #
    users.dialog.router,
    users.user.dialog.router,
    #
    # Other routers
    #
    extra.test.router,
    extra.member.router,
]

__all__ = [
    "routers",
]
