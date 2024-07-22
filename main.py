import logging
from os import getenv
from sys import argv, exit

from interactions import (
    Client,
    Intents,
    listen,
)

log = logging.getLogger("defcon-internal")
bot = Client(intents=Intents.DEFAULT, logging_level=logging.WARNING)


@listen()
async def on_ready() -> None:
    """Notify that the bot is started."""
    log.info("Bot started.")


def get_token() -> str:
    """Try to read bot's token from environment or .env."""

    try:
        from dotenv import load_dotenv

        load_dotenv()
        no_dotenv = False
    except ImportError:
        no_dotenv = True

    token = getenv("DEFCON_BOT_TOKEN")

    if token is None:
        log.error("Token not found.\nPlease specify discord bot token via environment variable 'DEFCON_BOT_TOKEN'.")

        if no_dotenv:
            log.info("To read token from .env, install 'python-dotenv'")

        exit()

    return token


def get_developer_mode() -> bool:
    """Get if the bot is running in dev mode."""
    try:
        return argv[1] == "--dev"
    except IndexError:
        return False


DEV = get_developer_mode()

if __name__ == "__main__":
    if DEV:
        bot.load_extension("interactions.ext.jurigged")

    bot.load_extension("src.game_start")
    bot.start(token=get_token())
