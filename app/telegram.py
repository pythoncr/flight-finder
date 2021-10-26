import logging
from telethon.sync import TelegramClient
from telethon.sessions.memory import MemorySession

import utils

logging.basicConfig(format="%(asctime)s %(levelname)s %(name)s - %(message)s")
log = utils.config_logger(__name__, logging.DEBUG)

CONFIG = {
    "TELEGRAM_API_HASH": utils.get_parameter("TELEGRAM_API_HASH"),
    "TELEGRAM_API_ID": utils.get_parameter("TELEGRAM_API_ID"),
    "TELEGRAM_BOT_TOKEN": utils.get_parameter("TELEGRAM_BOT_TOKEN"),
    "TELEGRAM_CHANNEL_ID": int(utils.get_parameter("TELEGRAM_CHANNEL_ID")),
}


def send_message(data, origin, destination, adults, children, departure_date, arrival_date):
    message = f"\n-\xE2\x9C\x88 Ofertas de {origin} a {destination} para {adults} adultos y {children} niños del {departure_date} al {arrival_date} con la ruta:\n"
    for offer in data["offers"]:
        for path in offer["itinerary"]["routes"][0]["path"]:
            message += f"\n• {path['departure']} {path['timeStampDeparture']} >>> {path['arrival']} {path['timeStampArrival']} (duración total: {offer['itinerary']['routes'][0]['fullDuration']}) (operado por {path['airline']})"
        message += "\n"
        for path in offer["itinerary"]["routes"][1]["path"]:
            message += f"\n• {path['departure']} {path['timeStampDeparture']} <<< {path['arrival']} {path['timeStampArrival']} (duración total: {offer['itinerary']['routes'][0]['fullDuration']}) (operado por {path['airline']})"
        message += f"\nTiene un precio de {offer['price']}"

    session = MemorySession()
    client = TelegramClient(session, CONFIG["TELEGRAM_API_ID"], CONFIG["TELEGRAM_API_HASH"])
    client.start(bot_token=CONFIG["TELEGRAM_BOT_TOKEN"])
    client.send_message(CONFIG["TELEGRAM_CHANNEL_ID"], message)
