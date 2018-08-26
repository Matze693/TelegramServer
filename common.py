import logging

LOGGING_LEVEL = logging.DEBUG
LOGGING_FORMAT = '%(asctime)s | %(levelname)-8s | %(message)s'


def get_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(LOGGING_LEVEL)
    handler = logging.StreamHandler()
    handler.setLevel(LOGGING_LEVEL)
    handler.setFormatter(logging.Formatter(LOGGING_FORMAT))
    logger.addHandler(handler)
    return logger
