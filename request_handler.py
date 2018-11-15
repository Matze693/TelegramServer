from enum import Enum
from socketserver import BaseRequestHandler

# logger
from common import get_logger

logger = get_logger(__name__)

ADMINS = [110086856]


class RequestHandler(BaseRequestHandler):

    class Response(Enum):
        Error = 'Error'
        Success = 'Success'

    def handle(self):
        data = self.request.recv(1024).strip().decode('utf-8')
        logger.info('Incoming message from client {}'.format(self.client_address))
        logger.info('<< "{}"'.format(data))

        # data = 'SenderName|Group|Level|DataType|Message'

        # check response structure
        if data.count('|') < 4:
            self.send_response(RequestHandler.Response.Error, 'Invalid command structure')
            return
        sender_name, group, level, data_type, message = data.split('|', 4)
        group = group.upper()
        level = level.upper()
        data_type = data_type.upper()

        # check sender_name
        if sender_name is '':
            self.send_response(RequestHandler.Response.Error, 'Empty sender name')
            return

        # check group
        if group not in ['ADMINS']:
            self.send_response(RequestHandler.Response.Error, 'Invalid group')
            return

        # check level
        if level not in ['ERROR', 'WARNING', 'INFO']:
            self.send_response(RequestHandler.Response.Error, 'Invalid level')
            return

        # data type for testing
        if data_type == 'TEST':
            self.send_response(RequestHandler.Response.Success)
            return

        # check data type
        if data_type == 'TEXT':
            if group == 'ADMINS':
                for admin in ADMINS:
                    self.server.dispatcher.bot.send_message(admin, data)
        else:
            self.send_response(RequestHandler.Response.Error, 'Invalid data type')
            return

        self.send_response(RequestHandler.Response.Success)
        return

    def send_response(self, response, message=''):
        data = '{}|{}'.format(response.value, message)
        logger.info('Send message to client {}'.format(self.client_address))
        logger.info('>> "{}"'.format(data))
        self.request.sendall(bytes(data, 'utf-8'))
