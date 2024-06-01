from __future__ import annotations

import os

from loguru import logger
from telegram import Update
from telegram.ext import Application
from telegram.ext import CommandHandler
from telegram.ext import ContextTypes

from .utils import get_ticker_string


class Bot:
    def __init__(self, token: str) -> None:
        self.app = Application.builder().token(token).build()
        self.app.add_handler(CommandHandler("yf", self.query_ticker))
        self.app.run_polling(allowed_updates=Update.ALL_TYPES)

    @classmethod
    def from_env(cls):
        token = os.getenv("BOT_TOKEN")
        if token is None:
            raise ValueError("BOT_TOKEN is not set")

        return cls(token=token)

    async def query_ticker(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        logger.info(f"Received message: {update.message.text}")

        symbols = update.message.text.lstrip("/yf").strip().upper().split(" ")

        logger.info(f"Querying symbols: {symbols}")
        reply_text = "\n".join([get_ticker_string(s) for s in symbols])

        await update.message.reply_text(reply_text)
