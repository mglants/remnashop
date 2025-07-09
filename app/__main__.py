import uvicorn
from fastapi import FastAPI

from app.core.config import AppConfig
from app.core.logger import setup_logger
from app.factories import (
    create_app,
    create_bot,
    create_container,
    create_dispatcher,
    create_middlewares,
    create_redis,
    create_remnawave,
    create_session_pool,
)


def build_application() -> FastAPI:
    setup_logger()
    config = AppConfig.get()

    redis = create_redis(url=config.redis.dsn)
    session_pool = create_session_pool(config)

    bot = create_bot(token=config.bot.token.get_secret_value())
    remnawave = create_remnawave(config)
    middlewares = create_middlewares(config)
    i18n_middleware = middlewares.get_i18n_middleware()

    container = create_container(
        bot=bot,
        config=config,
        redis=redis,
        session_pool=session_pool,
        i18n=i18n_middleware,
        remnawave=remnawave,
    )

    dispatcher = create_dispatcher(container, middlewares)
    app: FastAPI = create_app(dispatcher=dispatcher, bot=bot, config=config)
    return app


app: FastAPI = build_application()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
