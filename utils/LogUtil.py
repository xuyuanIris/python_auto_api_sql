import logging
import os

from config.Conf import RunConfig, PathConfig

if RunConfig.log_level == 'CRITICAL':
    _log_level = logging.CRITICAL
elif RunConfig.log_level == 'ERROR':
    _log_level = logging.ERROR
elif RunConfig.log_level == 'WARNING':
    _log_level = logging.WARNING
elif RunConfig.log_level == 'INFO':
    _log_level = logging.INFO
elif RunConfig.log_level == 'DEBUG':
    _log_level = logging.DEBUG
elif RunConfig.log_level == 'NOTSET':
    _log_level = logging.NOTSET
else:
    _log_level = logging.INFO

_out_console = True if RunConfig.log_out_console else False


class Log:
    """日志"""
    file_path = os.path.join(PathConfig.log, 'output.log')

    logger = logging.getLogger(__name__)
    logger.setLevel(level=_log_level)
    handler1 = logging.FileHandler(file_path, encoding='utf-8')
    datefmt = '%Y/%m/%d %H:%M:%S'
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(module)s - %(lineno)d - %(message)s')
    handler1.setFormatter(formatter)
    logger.addHandler(handler1)

    if _out_console:
        handler2 = logging.StreamHandler()
        handler2.setFormatter(formatter)
        logger.addHandler(handler2)


if __name__ == '__main__':
    logger = Log.logger
    logger.info('This is a log info')
    logger.debug('Debugging')
    logger.warning('Warning exists')
    logger.info('Finish')
