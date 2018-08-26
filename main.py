import configparser
import signal

from common import get_logger
from telegram_server import TelegramServer

logger = get_logger(__name__)


def signal_handler(sig, frame):
    logger.debug('User aborted server')


def main():
    logger.debug('Start program')
    signal.signal(signal.SIGINT, signal_handler)

    bot_config = configparser.ConfigParser()
    bot_config.read('bot.config')

    server = TelegramServer(token=bot_config['BOT']['TOKEN'])
    server.start()
    signal.pause()
    server.stop()

    logger.debug('Exit program')


if __name__ == '__main__':
    main()
