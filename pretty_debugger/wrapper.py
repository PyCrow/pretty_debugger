import inspect
from logging import Logger, WARNING
from time import time

from .cache import PrettyCache
from .utils import log, non_expo, is_logger, is_default_logging, is_loguru


def pretty_wrapper(
        logger: Logger,
        debug_level: int = None,
        round_exec_time: int = 4,
):
    """
    Wraps a function to log its execution, including all args, kwargs,
    execution result, and errors.

    Wrapper does not make any changes that affect the result of
    code execution or errors.

    :param logger: Logger (of default 'logging' or 'loguru' module)
        with encoding 'utf-8'.

    :param debug_level: Custom debug level. If not specified, the
        logger debug level or WARNING level is used, whichever is higher.

    :param round_exec_time: Round the execution time to N after the decimal point

    :returns: Wrapped function
    """
    # Validate logger
    if not is_logger(logger):
        raise TypeError("Logger object must contain a 'level' int attribute"
                        " and a 'log' method.")

    if debug_level is None:
        if is_default_logging(logger):
            # Default logging support
            debug_level = max(logger.level, WARNING)
        elif is_loguru(logger):
            # Loguru support
            debug_level = logger._core.min_level
        else:
            raise TypeError(f"Unsupported logger type: {type(logger)}")

    def _wrapper(func):
        cache = PrettyCache()

        sep = '  '

        def _logged_function(*args, **kwargs):
            nonlocal logger, debug_level

            get_prefix = lambda: f"┊{sep}" * cache.level
            prefix = get_prefix()

            # Start line
            if cache.level == 0:
                log(logger, debug_level, "┯")

            # Print args and kwargs
            if not args and not kwargs:
                log(logger, debug_level, f"{prefix}├─►{func.__name__}()")
            else:
                log(logger, debug_level, f"{prefix}├─►{func.__name__}(")
                args_kwargs = dict(zip(
                    list(inspect.signature(func).parameters.keys()),
                    args
                ))
                args_kwargs.update(kwargs)
                for k, v in args_kwargs.items():
                    log(logger, debug_level, f"{prefix}│{sep * 2}{k}={v},")
                log(logger, debug_level, f"{prefix}│{sep})")
            cache.level += 1

            # Execution
            start_time = time()
            msg = "<pretty_debugger: UNHANDLED EXCEPTION OCCURRED>"  # var to avoid NameError
            try:
                result = func(*args, **kwargs)
            except Exception as e:
                msg = f"X <{repr(e)}>"
                raise
            else:
                msg = f"► {result}"
            finally:
                stop_time = non_expo(time() - start_time, round_exec_time)
                log(logger, debug_level, f"{get_prefix()}└{msg}  ({stop_time}s)")

                cache.level -= 1

                # Finish line
                if cache.level == 0:
                    log(logger, debug_level, "┷")

            return result
        return _logged_function
    return _wrapper