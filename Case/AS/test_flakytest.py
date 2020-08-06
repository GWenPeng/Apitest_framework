from flaky import flaky
import random
import pytest
import time


def delay(*args):
    print(args)
    time.sleep(1)


def is_not_crash(error, *args):
    print(error, args)
    return not issubclass(error[0], AssertionError)


@flaky(max_runs=3, min_passes=1, rerun_filter=is_not_crash)
class Test_rerun(object):
    def test_flaky_case(self):
        assert int(random.random() * 7) == 1

    def test_flaky_case2(self):
        assert 3 == 3
