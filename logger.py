import logging

def get_logger():
    log = logging.getLogger('')
    log.setLevel(logging.DEBUG)
    logger = logging.StreamHandler()
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(levelname)s - %(funcName)s() - %(module)s - %(lineno)d - %(message)s')
    logger.setFormatter(formatter)
    log.addHandler(logger)
    return log

