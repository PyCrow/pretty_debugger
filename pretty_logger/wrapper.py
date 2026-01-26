import inspect
from logging import Logger, WARNING
from time import time

from .cache import PrettyCache


def pretty_wrapper(
        logger: Logger,
        debug_level: int = None,
        round_exec_time: int = 6,
):
    """
    Wraps a function to log its execution, including all args, kwargs,
    execution result, and errors.

    Wrapper does not make any changes that affect the result of
    code execution or errors.

    Example:
    ```
    ┯
    ├─⮞foobar(
    │    some_arg=0,
    │  )
    ┊  ├─⮞plus_one(
    ┊  │    some_arg=0,
    ┊  │  )
    ┊  ┊  └⮞1  (1.0152s)
    ┊  ├─⮞exception_func(
    ┊  │    this_is_kwarg=True,
    ┊  │  )
    ┊  ┊  └X <Exception('SOME TEST EXCEPTION')>  (0.0s)
    ┊  └X <Exception('SOME TEST EXCEPTION')>  (1.0152s)
    ┷
    ```

    :param logger: Logger object must contain the 'level' attribute,
        the 'log' method, and HAVE THE 'utf-8' ENCODING.

    :param debug_level: Custom debug level. If not specified, the
        logger debug level or WARNING level is used, whichever is higher.

    :param round_exec_time: Round the execution time to N after the decimal point

    :returns: Wrapped function
    """
    # Validate logger
    if not PrettyCache.is_logger(logger):
        raise TypeError("Logger object must contain a 'level' attribute"
                        " and a 'log' method.")
    if debug_level is None:
        debug_level = max(logger.level, WARNING)

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
            start_time = time()
            msg = "<pretty_wrapper: UNHANDLED EXCEPTION OCCURRED>"  # var to avoid NameError
            try:
                result = func(*args, **kwargs)
            except Exception as e:
                msg = f"X <{repr(e)}>"
                raise
            else:
                msg = f"⮞{result}"
            finally:
                stop_time = round(time() - start_time, round_exec_time)
                logger.log(debug_level,
                           f"{get_prefix()}└{msg}  ({stop_time}s)")

                cache.level -= 1

                # Finish line
                if cache.level == 0:
                    logger.log(debug_level, "┷")

            return result
        return _logged_function
    return _wrapper