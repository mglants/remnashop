from aiogram import Bot, Dispatcher
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.core.config import AppConfig
from app.endpoints import TelegramRequestHandler
from app.lifespan import lifespan


def create_app(dispatcher: Dispatcher, bot: Bot, config: AppConfig) -> FastAPI:
    app: FastAPI = FastAPI(lifespan=lifespan)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=config.origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    for key, value in dispatcher.workflow_data.items():
        setattr(app.state, key, value)

    app.state.dispatcher = dispatcher
    app.state.bot = bot

    tg_webhook_handler = TelegramRequestHandler(
        dispatcher=dispatcher,
        bot=bot,
        path=config.bot.webhook_path,
        secret_token=config.bot.secret_token.get_secret_value(),
    )
    app.state.tg_webhook_handler = tg_webhook_handler
    app.include_router(tg_webhook_handler.router)

    dispatcher.workflow_data.update(app=app)
    return app
