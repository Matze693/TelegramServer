from threading import Thread

from telegram.ext import Updater

# logger
from common import get_logger
from server import Server

logger = get_logger(__name__)


class TelegramServer:

    def __init__(self, token, host='', port=9999):
        self.telegram = Telegram(token=token)
        self.server = Server(host, port, self.telegram.dispatcher)

    def start(self):
        self.telegram.start()
        self.server.start()

    def stop(self):
        self.server.stop()
        self.telegram.stop()
        self.server.join()
        self.telegram.join()


class Telegram(Thread):

    def __init__(self, token):
        Thread.__init__(self)
        self.daemon = True
        self.updater = Updater(token=token)
        self.dispatcher = self.updater.dispatcher

    def run(self):
        logger.debug('telegram thread is running...')
        self.updater.start_polling(poll_interval=0.1, timeout=3)

    def stop(self):
        logger.debug('telegram thread will be stopped')
        self.updater.stop()
        logger.debug('telegram thread is killed')
