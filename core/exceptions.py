""" custom exceptions for FEBS """
from core.logger import logger


class MyLoggerException(Exception):
    """ class to automatically log to file """
    def __init__(self, msg, *args, **kwargs):
        super().__init__(msg, *args, **kwargs)
        # log to file
        logger.exception(f"{type(self)}: {msg}")


class ConfigNotProvided(MyLoggerException):
    """ raise when no config_file provided for main_model """


class BadJsonConfig(MyLoggerException):
    """ raise when config file is wrong """
