import inspect
import logging
from logging import Logger

from .cache import PrettyCache


def pretty_wrapper(logger: Logger, debug_level: int = None):
    """
    Wraps a function to log its execution, including all args, kwargs,
    execution result, and errors.

    Wrapper does not make any changes that affect the result of
    code execution or errors.

    Example:
    ┯
    ├─⮞foobar(
    │    some_arg=0,
    │  )
    ┊  ├─⮞plus_one(
    ┊  │    some_arg=0,
    ┊  │  )
    ┊  ┊  └⮞1
    ┊  ├─⮞exception_func(
    ┊  │    this_is_kwarg=True,
    ┊  │  )
    ┊  ┊  └X <Exception('SOME TEST EXCEPTION')>
    ┊  └X <Exception('SOME TEST EXCEPTION')>
    ┷

    :param logger: Logger object must contain a 'level' attribute and a 'log' method.
    :param debug_level: Custom debug level. If not specified, the
        logger debug level or WARNING level is used, whichever is higher.
    :return: Wrapped function
    """
    # Validate logger
    if not PrettyCache.is_logger(logger):
        raise TypeError("Logger object must contain a 'level' attribute"
                        " and a 'log' method.")
    if debug_level is None:
        debug_level = max(logger.level, logging.WARNING)
    print(logger.level)
    print(debug_level)

    def _wrapper(func):
        cache = PrettyCache()

        sep = '  '

        def _logged_function(*args, **kwargs):
            nonlocal logger, debug_level

            get_prefix = lambda: f"┊{sep}" * cache.level
            prefix = get_prefix()

            # Start line
            if cache.level == 0:
                logger.log(debug_level, "┯")

            # Print args and kwargs
            if not args and not kwargs:
                logger.log(debug_level, f"{prefix}├─⮞{func.__name__}()")
            else:
                logger.log(debug_level, f"{prefix}├─⮞{func.__name__}(")
                args_kwargs = dict(zip(
                    list(inspect.signature(func).parameters.keys()),
                    args
                ))
                args_kwargs.update(kwargs)
                for k, v in args_kwargs.items():
                    logger.log(debug_level, f"{prefix}│{sep * 2}{k}={v},")
                logger.log(debug_level, f"{prefix}│{sep})")
            cache.level += 1

            # Execution
            try:
                result = func(*args, **kwargs)
            except Exception as e:
                logger.log(debug_level, f"{get_prefix()}└X <{repr(e)}>")
                raise
            else:
                logger.log(debug_level, f"{get_prefix()}└⮞{result}")
            finally:
                cache.level -= 1

                # Finish line
                if cache.level == 0:
                    logger.log(debug_level, "┷")

            return result
        return _logged_function
    return _wrapper