import os
from urubu import UrubuError, project
from urubu.project import _error

from . import cd, raises_kind

def test_undef_ref():
    with cd('undef_ref'):
        with raises_kind(UrubuError, _error.undef_ref):
            project.build()
