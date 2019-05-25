from threading import Thread
import logging

from telegram.ext import Updater

from server import Server


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
        logging.debug('telegram thread is running...')
        self.updater.start_polling(poll_interval=0.1, timeout=3)

    def stop(self):
        logging.debug('telegram thread will be stopped')
        self.updater.stop()
        logging.debug('telegram thread is killed')
