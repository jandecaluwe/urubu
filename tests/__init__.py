
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


