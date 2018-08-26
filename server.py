from socketserver import ThreadingTCPServer
from threading import Thread

# logger
from common import get_logger
from request_handler import RequestHandler

logger = get_logger(__name__)

ADMIN_ID = '110086856'


class Server(Thread):

    def __init__(self, host, port, dispatcher):
        Thread.__init__(self)
        self.daemon = True
        self.server = ThreadingTCPServer((host, port), RequestHandler, bind_and_activate=False)
        self.server.allow_reuse_address = True
        self.server.server_bind()
        self.server.server_activate()
        self.server.dispatcher = dispatcher

    def run(self):
        logger.debug('server thread is running...')
        self.server.serve_forever()

    def stop(self):
        logger.debug('server thread will be stopped')
        self.server.shutdown()
        self.server.server_close()
        logger.debug('server thread is killed')
