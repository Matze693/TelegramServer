import socket
import logging
import unittest
import configparser

import common
common.LOGGING_LEVEL = logging.DEBUG

from telegram_server import TelegramServer


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
        self.sendData('||||')
        response, message = self.receiveData().split('|')
        self.assertEqual('Error', response)

    def test_send_invalid_sender_name(self):
        self.sendData('|||')
        response, message = self.receiveData().split('|')
        self.assertEqual('Error', response)

    def test_send_invalid_group(self):
        self.sendData('TestSender|Group|Text|Message')
        response, message = self.receiveData().split('|')
        self.assertEqual('Error', response)

    def test_send_invalid_data_type(self):
        self.sendData('TestSender|Admins|DataType|Message')
        response, message = self.receiveData().split('|')
        self.assertEqual('Error', response)

    def test_send_valid_data(self):
        self.sendData('TestSender|Admins|Test|Message|')
        response, message = self.receiveData().split('|')
        self.assertEqual('Success', response)

    def tearDown(self):
        self.client.close()

    @classmethod
    def tearDownClass(cls):
        cls.server.stop()
