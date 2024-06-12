import logging
import sys
import os


log_level = None


def get_logger(name):
    global log_level
    if log_level is None:
        init_logging()

    logger = logging.getLogger(name)
    logger.setLevel(log_level)
    return logger


def init_logging():
    global log_level

    log_level_name = os.getenv('LOG_LEVEL', 'info')
    log_level_name = log_level_name.lower()
    if log_level_name == 'info':
        log_level = logging.INFO
    elif log_level_name == 'debug':
        log_level = logging.DEBUG
    elif log_level_name == 'warning':
        log_level = logging.WARNING
    elif log_level_name == 'error':
        log_level = logging.ERROR
    else:
        logging.critical(f'Unhanled log level {log_level_name}')
        sys.exit()

    log_format = "%(asctime)s :: %(filename)s:%(lineno)d :: %(levelname)s :: %(message)s"
    logging.basicConfig(format=log_format)
