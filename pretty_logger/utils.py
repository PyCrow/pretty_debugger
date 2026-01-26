from logging import makeLogRecord


non_expo = lambda n, round_to: f"%.{round_to}f" % n


log = lambda logger, level, msg, *args: logger.handle(
    makeLogRecord({
        'args': args,
        'levelname': "PRETTY",
        'levelno': level,
        'lineno': 0,
        'msg': msg,
        'name': "PRETTY",  # Logger name
    })
)