import logging
from telethon.sync import TelegramClient

import utils

CONFIG = {
    "TELEGRAM_API_HASH": utils.get_parameter("TELEGRAM_API_HASH"),
    "TELEGRAM_API_ID": utils.get_parameter("TELEGRAM_API_ID"),
    "TELEGRAM_BOT_TOKEN": utils.get_parameter("TELEGRAM_BOT_TOKEN"),
    "TELEGRAM_CHANNEL_ID": utils.get_parameter("TELEGRAM_CHANNEL_ID"),
}


def send_message(message):
    client = TelegramClient("flight-finder", CONFIG["TELEGRAM_API_ID"], CONFIG["TELEGRAM_API_HASH"])
    client.start(bot_token=CONFIG["TELEGRAM_BOT_TOKEN"])
    client.send_message(CONFIG["TELEGRAM_CHANNEL_ID"], message)
