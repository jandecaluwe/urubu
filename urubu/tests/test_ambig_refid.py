import os
from urubu import UrubuError, project
from urubu.project import _error

from urubu.tests import cd, raises_kind

def test_ambig_refid():
    with cd('ambig_refid'):
        with raises_kind(UrubuError, _error.ambig_refid):
            project.build()
