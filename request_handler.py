from enum import Enum
from socketserver import BaseRequestHandler

# logger
from common import get_logger

logger = get_logger(__name__)

ADMINS = [110086856]


class RequestHandler(BaseRequestHandler):
    class StringEnum(Enum):
        @classmethod
        def has_value(cls, value):
            return any(value == item.value for item in cls)

    class Response(StringEnum):
        Error = 'Error'
        Success = 'Success'

    class Group(StringEnum):
        Admin = 'Admin'

    class Level(StringEnum):
        Error = 'Error'
        Warning = 'Warning'
        Info = 'Info'

    class DataType(StringEnum):
        Test = 'Test'
        Text = 'Text'

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
        group = group.title()
        level = level.title()
        data_type = data_type.title()

        # check sender_name
        if sender_name is '':
            self.send_response(RequestHandler.Response.Error, 'Empty sender name')
            return

        # check group
        if not RequestHandler.Group.has_value(group):
            self.send_response(RequestHandler.Response.Error, 'Invalid group')
            return

        # check level
        if not RequestHandler.Level.has_value(level):
            self.send_response(RequestHandler.Response.Error, 'Invalid level')
            return

        # check data type
        if not RequestHandler.DataType.has_value(data_type):
            self.send_response(RequestHandler.Response.Error, 'Invalid data type')
            return

        if RequestHandler.DataType[data_type] is RequestHandler.DataType.Test:
            self.send_response(RequestHandler.Response.Success)
            return

        if RequestHandler.DataType[data_type] is RequestHandler.DataType.Text:
            if RequestHandler.Group[group] is RequestHandler.Group.Admin:
                for admin in ADMINS:
                    self.server.dispatcher.bot.send_message(admin, data)

        self.send_response(RequestHandler.Response.Success)
        return

    def send_response(self, response, message=''):
        data = '{}|{}'.format(response.value, message)
        logger.info('Send message to client {}'.format(self.client_address))
        logger.info('>> "{}"'.format(data))
        self.request.sendall(bytes(data, 'utf-8'))
