import os
from urubu import UrubuError, project
from urubu.project import _error

from urubu.tests import cd, raises_kind

def test_date_format():
    with cd('date_format'):
        with raises_kind(UrubuError, _error.date_format):
            project.build()
