import logging, json_config, file_handler
from dataclasses import dataclass
from queue import Queue
from logging.config import dictConfig
from logging.handlers import TimedRotatingFileHandler
from os.path import dirname


@dataclass
class LogConfig:
    version : int
    log_format : str
    logger_level : int
    console_level : int
    gui_level : int
    file_level : int
    path : str
    log_name : str
    log_extension : str


try:
    template = """{
    "version": 1,
    "disable_existing_loggers": false,
    "formatters": {
        "brief": {
            "format" : "[%(asctime)s - %(levelname)s] %(name)-12s %(message)s",
            "datefmt" : "%Y-%m-%d %H:%M:%S"
        },
        "precise": {
            "format": "[%(asctime)s - %(levelname)s] %(name)-12s %(funcName)-30s %(message)s",
            "datefmt" : "%Y-%m-%d %H:%M:%S"
        }
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "brief",
            "level": "DEBUG",
            "stream": "ext://sys.stdout"
        },
        "file_handler": {
            "class" : "logger.TimedRotatingFileHandlerCustomNamer",
            "formatter" : "precise",
            "level" : "INFO",
            "filename" : "./Log/Log.log",
            "when": "d",
            "interval" : 1
        },
        "queue_handler" : {
            "class" : "logger.LogQueuer",
            "formatter" : "brief",
            "level" : "DEBUG"
        }
    },
    "root": {
        "handlers": [
            "console", "file_handler", "queue_handler"
        ],
        "level": "DEBUG"
    }
}"""
    config = json_config.load_json_config('logger_config.json', template)
    for handler in config['handlers'].values():
        if 'filename' in handler.keys():
            file_handler.check_create_dir(dirname(handler['filename']))
except Exception as error:
    print(f'Config loading error {error}')
    exit()


def logger_setup(logger=logging.Logger | None, log_queue=Queue | None):
    try:
        dictConfig(config)
        if not logger == None:
            # logger = add_log_queuer(logger, log_queue)
            logger = add_handler(logger, LogQueuer, log_queue)
    except Exception as error:
        print(error)
        exit()


def add_handler(current_logger=logging.Logger, handler_class=logging.Handler, log_queue=None | Queue):
    formatter =''
    level = ''
    for handler in current_logger.handlers:
        if isinstance(handler, handler_class):
            formatter = handler.formatter
            level = handler.level
            current_logger.handlers.remove(handler)
    if not formatter and not level:
        formatter = current_logger.handlers[0].formatter
        level = current_logger.handlers[0].level
    if log_queue == None:
        log_handler = handler_class()
    else:
        log_handler = handler_class(log_queue)
    log_handler.setFormatter(formatter)
    log_handler.setLevel(level)
    current_logger.handlers.append(log_handler)
    return current_logger


def add_log_queuer(current_logger=logging.Logger, log_queue=Queue()):
    formatter =''
    level = ''
    for handler in current_logger.handlers:
        if isinstance(handler, LogQueuer):
            formatter = handler.formatter
            level = handler.level
            current_logger.handlers.remove(handler)
    if not formatter and not level:
        formatter = current_logger.handlers[0].formatter
        level = current_logger.handlers[0].level
    log_handler = LogQueuer(log_queue)
    log_handler.setFormatter(formatter)
    log_handler.setLevel(level)
    current_logger.handlers.append(log_handler)
    return current_logger


class LogQueuer(logging.Handler):
    def __init__(self, log_queue=Queue()) -> None:
        logging.Handler.__init__(self)
        self.log_queue = log_queue

    
    def emit(self, record):
        if self.log_queue.qsize() >= 100:
            self.log_queue.get(block=False)
        self.log_queue.put(self.format(record))


class TimedRotatingFileHandlerCustomNamer(TimedRotatingFileHandler):
    def __init__(self, filename: str, when: str = "h", interval: int = 1, backupCount: int = 0, encoding: str | None = None, delay: bool = False, utc: bool = False, atTime: None = None, errors: str | None = None) -> None:
        extension = filename.split('.')[-1]
        self.namer = lambda filename : f'{filename.replace(f".{extension}", "")}.{extension}'
        super().__init__(filename, when, interval, backupCount, encoding, delay, utc, atTime, errors)
        

if __name__ == '__main__':
    logger_setup()
    loggers = logging.getLogger()

    loggers.debug('Test')
    loggers.info('Done')