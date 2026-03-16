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
```text
┯
├─► foo(  ---  [NONREPO/test.py:6]
│      bar='world',
│   )
┊   └► 'Hello, world'  [0.0000s]
┷
```

Output when using nested wrapped functions:
```text
┯
├─► main_task()  ---  [NONREPO/test.py:12]
┊   ├─► get_data(  ---  [NONREPO/test.py:24]
┊   │      arg=42,
┊   │      kwarg='active',
┊   │   )
┊   ┊   └► 420  [0.0000s]
┊   ├─► check_status()  ---  [NONREPO/test.py:29]
┊   ┊   └► None  [0.0000s]
┊   ├─► generate_error()  ---  [NONREPO/test.py:34]
┊   ┊   └X <RuntimeError('Critical Failure')>  [0.0000s]
┊   └X <RuntimeError('Critical Failure')>  [0.0003s]
┷
```

Param `logger`: Logger (of default 'logging' or 'loguru' module)
    with encoding 'utf-8'.

Param `debug_level`: Custom debug level. If not specified, the
    logger debug level or WARNING level is used, whichever is higher.

Param `round_exec_time`: Round the execution time to N after the decimal point

Returns: Wrapped function

---

Zero-dependency:
    Package does not require installation of additional libraries.
    Only default packages are included:
    [inspect](https://docs.python.org/3/library/inspect.html),
    [logging](https://docs.python.org/3/library/logging.html),
    [os](https://docs.python.org/3/library/os.html),
    and [time](https://docs.python.org/3/library/time.html).