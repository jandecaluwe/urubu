import contextlib, os

@contextlib.contextmanager
def cd(path):
    """context manager to change directory temporarily.
       From activestate recipes.

    """

    prev_cwd = os.getcwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(prev_cwd)



# reused from MyHDL
import pytest

class raises_kind(object):
    def __init__(self, exc, kind):
        self.exc = exc
        self.kind = kind

    def __enter__(self):
        return None

    def __exit__(self, *tp):
        __tracebackhide__ = True
        if tp[0] is None:
            pytest.fail("DID NOT RAISE")
        assert tp[1].kind == self.kind
        return issubclass(tp[0], self.exc)
