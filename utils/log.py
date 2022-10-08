# coding: utf-8
import logging

logger = logging.getLogger('nibl')
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter(logging.BASIC_FORMAT)

class MyLoggerHandler(logging.Handler):
    def __init__(self, output):
       self.output = output
       logging.Handler.__init__(self)

    def emit(self,record):
        msg = self.format(record)
        self.output(msg)

def getLogger(output):
    logger.addHandler(MyLoggerHandler(output))
    return logger