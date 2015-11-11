import os
from urubu import UrubuError, project
from urubu.project import _error

from . import cd, raises_kind

def test_ambig_ref():
    with cd('ambig_ref'):
        with raises_kind(UrubuError, _error.ambig_ref):
            project.build()
