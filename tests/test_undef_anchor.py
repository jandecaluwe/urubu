import os
from urubu import UrubuError, project

from . import cd

def test_undef_anchor():
    with cd('undef_anchor'):
        try:
            project.build()
        except UrubuError:
            pass
