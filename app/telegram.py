import logging
from telethon.sync import TelegramClient

import utils

logging.basicConfig(format="%(asctime)s %(levelname)s %(name)s - %(message)s")
log = utils.config_logger(__name__, logging.DEBUG)

CONFIG = {
    "TELEGRAM_API_HASH": utils.get_parameter("TELEGRAM_API_HASH"),
    "TELEGRAM_API_IP": utils.get_parameter("TELEGRAM_API_IP"),
    "TELEGRAM_BOT_TOKEN": utils.get_parameter("TELEGRAM_BOT_TOKEN"),
    "TELEGRAM_CHANNEL_ID": utils.get_parameter("TELEGRAM_CHANNEL_ID"),
}


def send_message(message):
    log.info(f"message to send: {message}")
    client = TelegramClient("flight-finder", CONFIG["TELEGRAM_API_IP"], CONFIG["TELEGRAM_API_HASH"])
    client.start(bot_token=CONFIG["TELEGRAM_BOT_TOKEN"])
    m = client.send_message(CONFIG["TELEGRAM_CHANNEL_ID"], message)
    log.info(f"all good? {m}")
