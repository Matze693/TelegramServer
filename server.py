from socketserver import ThreadingTCPServer
from threading import Thread
import logging

from request_handler import RequestHandler

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
        logging.debug('server thread is running...')
        self.server.serve_forever()

    def stop(self):
        logging.debug('server thread will be stopped')
        self.server.shutdown()
        self.server.server_close()
        logging.debug('server thread is killed')
