import os
from urubu import UrubuError, project
from urubu.project import _error

from urubu.tests import cd, raises_kind

def test_undef_reflink_title():
    with cd('undef_reflink_title'):
        with raises_kind(UrubuError, _error.undef_reflink_key):
            project.build()

def test_undef_reflink_url():
    with cd('undef_reflink_url'):
        with raises_kind(UrubuError, _error.undef_reflink_key):
            project.build()
