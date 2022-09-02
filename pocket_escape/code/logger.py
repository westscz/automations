import logging


def configure_logger(name):
    log = logging.getLogger(name)
    log.setLevel(logging.INFO)
    stream = logging.StreamHandler()
    log.addHandler(stream)
    return log
