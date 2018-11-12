from enum import Enum
from socketserver import BaseRequestHandler

# logger
from common import get_logger

logger = get_logger(__name__)


class RequestHandler(BaseRequestHandler):

    class Response(Enum):
        Error = 'Error'
        Success = 'Success'

    def handle(self):
        data = self.request.recv(1024).strip().decode('utf-8')
        logger.info('Incoming message from client {}'.format(self.client_address))
        logger.info('<< "{}"'.format(data))

        # data = 'SenderName|Group|DataType|Message'

        # check response structure
        if data.count('|') < 3:
            self.send_response(RequestHandler.Response.Error, 'Invalid command structure')
            return
        sender_name, group, data_type, message = data.split('|', 3)
        group = group.upper()
        data_type = data_type.upper()

        # check sender_name
        if sender_name is '':
            self.send_response(RequestHandler.Response.Error, 'Empty sender name')
            return

        # check group
        if group not in ['ADMINS']:
            self.send_response(RequestHandler.Response.Error, 'Invalid group')
            return

        # check data type
        if data_type not in ['TEXT', 'TEST']:
            self.send_response(RequestHandler.Response.Error, 'Invalid data type')
            return

        # handle data types
        if data_type == 'TEST':
            self.send_response(RequestHandler.Response.Success)
            return

    def send_response(self, response, message=''):
        data = '{}|{}'.format(response.value, message)
        logger.info('Send message to client {}'.format(self.client_address))
        logger.info('>> "{}"'.format(data))
        self.request.sendall(bytes(data, 'utf-8'))
