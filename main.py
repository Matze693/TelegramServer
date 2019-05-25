import logging
import configparser
import signal

from telegram_server import TelegramServer

# logging
console_logging = logging.StreamHandler()
console_logging.setLevel(logging.WARNING)

logging.basicConfig(level=logging.NOTSET,
                    handlers=[console_logging],
                    format='%(asctime)23s - %(levelname)8s - %(name)25s - %(funcName)25s - %(message)s'
                    )


def signal_handler(sig, frame):
    logging.debug('User aborted server')


def main():
    logging.debug('Start program')
    signal.signal(signal.SIGINT, signal_handler)

    bot_config = configparser.ConfigParser()
    bot_config.read('bot.config')

    server = TelegramServer(token=bot_config['BOT']['TOKEN'])
    server.start()
    signal.pause()
    server.stop()

    logging.debug('Exit program')


if __name__ == '__main__':
    main()
