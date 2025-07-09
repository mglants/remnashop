import hashlib

from aiogram import Bot, Dispatcher
from aiogram.methods import SetWebhook
from aiogram.types import WebhookInfo
from loguru import logger

from app.core.container import AppContainer
from app.core.utils import mjson


async def webhook_startup(bot: Bot, dispatcher: Dispatcher, container: AppContainer) -> None:
    safe_webhook_url = container.config.bot.safe_webhook_url(domain=container.config.domain)

    webhook = SetWebhook(
        url=container.config.bot.webhook_url(domain=container.config.domain).get_secret_value(),
        allowed_updates=dispatcher.resolve_used_update_types(),
        drop_pending_updates=container.config.bot.drop_pending_updates,
        secret_token=container.config.bot.secret_token.get_secret_value(),
    )

    webhook_hash: str = hashlib.sha256(mjson.bytes_encode(webhook.model_dump())).hexdigest()
    if await container.redis_repository.is_webhook_set(bot_id=bot.id, webhook_hash=webhook_hash):
        logger.info("Bot webhook setup skipped, already configured")
        logger.debug(f"Current webhook URL: '{safe_webhook_url}'")
        return

    if not await bot(webhook):
        raise RuntimeError(f"Failed to set bot webhook on URL '{safe_webhook_url}'")

    await container.redis_repository.clear_webhooks(bot_id=bot.id)
    await container.redis_repository.set_webhook(bot_id=bot.id, webhook_hash=webhook_hash)

    logger.info("Bot webhook set successfully")
    logger.debug(f"Webhook URL: '{safe_webhook_url}'")

    webhook_info: WebhookInfo = await bot.get_webhook_info()
    if webhook_info.last_error_message:
        logger.warning(f"Webhook has a last error message: {webhook_info.last_error_message}")


async def webhook_shutdown(bot: Bot, container: AppContainer) -> None:
    if not container.config.bot.reset_webhook:
        logger.debug("Bot webhook reset is disabled")
        return

    if await bot.delete_webhook():
        logger.info("Bot webhook deleted successfully")
        await container.redis_repository.clear_webhooks(bot_id=bot.id)
    else:
        logger.error("Failed to delete bot webhook")
