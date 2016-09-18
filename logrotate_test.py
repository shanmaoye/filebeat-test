import logging
import time
import commands
import os

log_format = '%(asctime)s %(filename)s[line:%(lineno)d]'\
    + ' %(levelname)s %(message)s'
# logging.basicConfig(level=logging.DEBUG,
#                     format=log_format,
#                     datefmt='%a, %d %b %Y %H:%M:%S',
#                     filename='/var/log/shanmao/shanmao.log',
#                     filemode='a')


def _size_of_file():
    print os.path.getsize("/var/log/shanmao/shanmao.log")


def _init_loghandler():
    formatter = logging.Formatter(log_format)
    infoLogger = logging.getLogger("infoLog")
    infoLogger.setLevel(logging.INFO)
    filename = '/var/log/shanmao/shanmao.log'
    infoHandler = logging.FileHandler(filename, 'a')
    infoHandler.setLevel(logging.INFO)
    infoHandler.setFormatter(formatter)
    infoLogger.addHandler(infoHandler)
    return infoLogger


def _close_handler(logger):
    handlers = logging._handlers.copy()
    for handler in handlers:
        logger.removeHandler(handler)
        handler.flush()
        handler.close()


def _init_registry_handler():
    formatter = logging.Formatter(log_format)
    infoLogger = logging.getLogger("regLog")
    infoLogger.setLevel(logging.INFO)
    filename = '/var/log/registry.log'
    infoHandler = logging.FileHandler(filename, 'w')
    infoHandler.setLevel(logging.INFO)
    infoHandler.setFormatter(formatter)
    infoLogger.addHandler(infoHandler)
    return infoLogger


def _write_registry_log(logger):
    msg = ''
    try:
        with open("/opt/filebeat-1.2.3-x86_64/.filebeat", 'r') as f:
            msg = f.read()
        logger.info(msg)
    except:
        logger.info("None")

if __name__ == '__main__':
    filebeatLogger = _init_registry_handler()
    infoLogger = _init_loghandler()
    max_line = 5000
    sleep_list = [1, 2, 3, 5, 7, 11, 13, 17, 23, 27]
    for i in range(1, max_line):
        time.sleep(0.1)
        infoLogger.info("This is test " + str(i))
        if i % 300 == 0:
            # _size_of_file()
            _close_handler(infoLogger)
            _write_registry_log(filebeatLogger)
            commands.getoutput("/etc/cron.daily/logrotate")
            _write_registry_log(filebeatLogger)
            infoLogger = _init_loghandler()
            index = int(i / 300)
            if index == len(sleep_list):
                break
            print index
            time.sleep(sleep_list[index])
            _write_registry_log(filebeatLogger)
    # commands.getoutput("/etc/cron.daily/logrotate")
