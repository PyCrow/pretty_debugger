from logging import makeLogRecord, Logger

PRETTY_LOGGER_NAME = "PRETTY"
PRETTY_LEVEL_NAME = "PRETTY"
PRETTY_LINENO = 0


def non_expo(n: float, round_to: int):
    return ("{:.%sf}" % round_to).format(n)


def is_logger(logger) -> bool:
    """ Checks if 'logger' has logging functionality:
    1. 'log' method
    """
    return (
        hasattr(logger, 'log')
        and callable(logger.log)
    )


def is_default_logging(logger) -> bool:
    return isinstance(logger, Logger)


def is_loguru(logger) -> bool:
    """ loguru.logger support """
    return (
        hasattr(logger, 'bind')
        and callable(logger.bind)

        and hasattr(logger, 'patch')
        and callable(logger.patch)

        and hasattr(logger, '_core')
        and hasattr(logger._core, 'min_level')
    )


def _update_level_line(record):
    record['level'].name = PRETTY_LEVEL_NAME
    record['line'] = PRETTY_LINENO


def log(logger, level: int, message: str, *args):
    if is_loguru(logger):
        logger.bind(logger_name=PRETTY_LEVEL_NAME)\
              .patch(_update_level_line)\
              .log(level, message)
    else:
        logger.handle(makeLogRecord({
            'args': args,
            'levelname': PRETTY_LEVEL_NAME,
            'levelno': level,
            'lineno': PRETTY_LINENO,
            'msg': message,
            'name': PRETTY_LOGGER_NAME,
        }))
