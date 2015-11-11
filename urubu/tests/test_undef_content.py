import os
from urubu import UrubuError, project
from urubu.project import _error

from urubu.tests import cd, raises_kind

def test_undef_content():
    with cd('undef_content'):
        with raises_kind(UrubuError, _error.undef_content):
            project.build()
