import logging
import unittest
from time import sleep

from pretty_logger import pretty_wrapper

logging.basicConfig(
    filename='pretty.log',
    format='%(message)s',
    encoding='utf-8',
)
logger = logging.getLogger(__name__)


@pretty_wrapper(logger)
def foobar(some_arg: int):
    plus_one(some_arg)
    exception_func(this_is_kwarg=True)

@pretty_wrapper(logger)
def plus_one(some_arg):
    sleep(1)
    return some_arg + 1

@pretty_wrapper(logger)
def exception_func(this_is_kwarg: bool):
    if this_is_kwarg:
        raise Exception("SOME TEST EXCEPTION")


class TestPrettyWrapper(unittest.TestCase):

    def test_pretty_wrapper(self):
        try:
            foobar(0)
        except Exception as e:
            assert str(e) == "SOME TEST EXCEPTION", "Unexpected exception"



if __name__ == '__main__':
    unittest.main()