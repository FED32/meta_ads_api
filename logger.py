import logging
import logging.handlers


def password_token_filter(log: logging.LogRecord) -> int:
    if 'password' in str(log.msg) or 'token' in str(log.msg):
        return 0
    else:
        return 1


def init_logger():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s - (%(filename)s:%(lineno)d)")

    sh = logging.StreamHandler()
    sh.setLevel(logging.INFO)
    sh.setFormatter(formatter)
    sh.addFilter(password_token_filter)

    fh = logging.handlers.RotatingFileHandler(filename="logs/logs.log", maxBytes=1000000, backupCount=10)
    fh.setLevel(logging.INFO)
    fh.setFormatter(formatter)
    fh.addFilter(password_token_filter)

    file_handler = logging.handlers.RotatingFileHandler(filename="logs/logs_error.log", maxBytes=1000000, backupCount=10)
    file_handler.setLevel(logging.ERROR)
    file_handler.setFormatter(formatter)
    file_handler.addFilter(password_token_filter)

    logger.addHandler(sh)
    logger.addHandler(fh)
    logger.addHandler(file_handler)

    return logger