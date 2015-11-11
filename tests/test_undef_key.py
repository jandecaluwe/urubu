import os
from urubu import UrubuError, project
from urubu.project import _error

from . import cd, raises_kind

def test_undef_key():
    with cd('undef_key'):
        with raises_kind(UrubuError, _error.undef_key):
            project.build()
