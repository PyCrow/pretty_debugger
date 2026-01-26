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

Param `logger`: Logger object must contain the 'level' attribute,
    the 'log' method, and HAVE THE 'utf-8' ENCODING.

Param `debug_level`: Custom debug level. If not specified, the
    logger debug level or WARNING level is used, whichever is higher.

Param `round_exec_time`: Round the execution time to N after the decimal point

Returns: Wrapped function