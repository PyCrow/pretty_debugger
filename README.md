Wraps a function to log its execution, including all args, kwargs,
execution result, and errors.

Wrapper does not make any changes that affect the result of
code execution or errors.

SUPPORTS: default 'logging.Logger' and 'loguru.logger'

Usage:
```python
import logging
from pretty_debugger import pretty_wrapper

logger = logging.getLogger(__name__)

@pretty_wrapper(logger)
def foo(bar):
    return f"Hello, {bar}"

foo("world")
```

Corresponding output:
```
┯
├─►foo(
│    bar=world,
│  )
┊  └► Hello, world  (0.0000s)
┷
```

Output when using nested wrapped functions:
```
┯
├─►foobar(
│    some_arg=0,
│  )
┊  ├─►plus_one(
┊  │    some_arg=0,
┊  │  )
┊  ┊  └► 1  (1.0011s)
┊  ├─►exception_func(
┊  │    this_is_kwarg=True,
┊  │  )
┊  ┊  └X <Exception('SOME TEST EXCEPTION')>  (0.0000s)
┊  └X <Exception('SOME TEST EXCEPTION')>  (1.0022s)
┷
```

Param `logger`: Logger (of default 'logging' or 'loguru' module)
    with encoding 'utf-8'.

Param `debug_level`: Custom debug level. If not specified, the
    logger debug level or WARNING level is used, whichever is higher.

Param `round_exec_time`: Round the execution time to N after the decimal point

Returns: Wrapped function

---

Zero-dependency: Package does not require installation of additional libraries