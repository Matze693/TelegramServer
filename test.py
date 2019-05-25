import configparser
import socket
import logging
import unittest
from threading import Thread

from telegram_server import TelegramServer


# logging
console_logging = logging.StreamHandler()
console_logging.setLevel(logging.NOTSET)

logging.basicConfig(level=logging.NOTSET,
                    handlers=[console_logging],
                    format='%(asctime)23s - %(levelname)8s - %(funcName)25s - %(message)s'
                    )


class ThreadTests(unittest.TestCase):
    class TestThread(Thread):

        def __init__(self):
            Thread.__init__(self)
            self.daemon = True
            self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client.connect(('127.0.0.1', 9999))
            self.response = None
            self.message = None

        def run(self):
            self.client.sendall(bytes('TestSender|Admin|Error|Test|Message', 'utf-8'))
            response, message = self.client.recv(4096).strip().decode('utf-8').split('|', 1)
            self.response = response
            self.message = message

    @classmethod
    def setUpClass(cls):
        bot_config = configparser.ConfigParser()
        bot_config.read('bot.config')
        cls.server = TelegramServer(token=bot_config['BOT']['TOKEN'])
        cls.server.start()
        cls.threads = list()
        threads = 1000
        for i in range(threads):
            cls.threads.append(ThreadTests.TestThread())

    def test_run(self):
        for thread in self.threads:
            thread.start()
        for thread in self.threads:
            thread.join()
        for thread in self.threads:
            self.assertEqual('Success', thread.response)

    @classmethod
    def tearDownClass(cls):
        cls.server.stop()


class Tests(unittest.TestCase):

    def sendData(self, data):
        self.client.sendall(bytes(data, 'utf-8'))

    def receiveData(self):
        return self.client.recv(4096).strip().decode('utf-8')

    @classmethod
    def setUpClass(cls):
        bot_config = configparser.ConfigParser()
        bot_config.read('bot.config')
        cls.server = TelegramServer(token=bot_config['BOT']['TOKEN'])
        cls.server.start()

    def setUp(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(('127.0.0.1', 9999))

    def test_send_invalid_structure(self):
        self.sendData('|')
        response, message = self.receiveData().split('|', 1)
        self.assertEqual('Error', response)

    def test_send_invalid_sender_name(self):
        self.sendData('||||')
        response, message = self.receiveData().split('|', 1)
        self.assertEqual('Error', response)

    def test_send_invalid_group(self):
        self.sendData('TestSender|Group|Level|Text|Message')
        response, message = self.receiveData().split('|', 1)
        self.assertEqual('Error', response)

    def test_send_invalid_level(self):
        self.sendData('TestSender|Admin|Level|Text|Message')
        response, message = self.receiveData().split('|', 1)
        self.assertEqual('Error', response)

    def test_send_invalid_data_type(self):
        self.sendData('TestSender|Admin|Error|DataType|Message')
        response, message = self.receiveData().split('|', 1)
        self.assertEqual('Error', response)

    def test_send_valid_data(self):
        self.sendData('TestSender|Admin|Error|Test|Message|')
        response, message = self.receiveData().split('|', 1)
        self.assertEqual('Success', response)

    def tearDown(self):
        self.client.close()

    @classmethod
    def tearDownClass(cls):
        cls.server.stop()


class TelegramTests(unittest.TestCase):

    def sendData(self, data):
        self.client.sendall(bytes(data, 'utf-8'))

    def receiveData(self):
        return self.client.recv(4096).strip().decode('utf-8')

    @classmethod
    def setUpClass(cls):
        bot_config = configparser.ConfigParser()
        bot_config.read('bot.config')
        cls.server = TelegramServer(token=bot_config['BOT']['TOKEN'])
        cls.server.start()

    def setUp(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(('127.0.0.1', 9999))

    def test_error(self):
        self.sendData('TestSender|Admin|Error|Text|error test message')
        response, message = self.receiveData().split('|', 1)
        self.assertEqual('Success', response)

    def test_warning(self):
        self.sendData('TestSender|Admin|Warning|Text|warning test message')
        response, message = self.receiveData().split('|', 1)
        self.assertEqual('Success', response)

    def test_info(self):
        self.sendData('TestSender|Admin|Info|Text|info test message')
        response, message = self.receiveData().split('|', 1)
        self.assertEqual('Success', response)

    def tearDown(self):
        self.client.close()

    @classmethod
    def tearDownClass(cls):
        cls.server.stop()
