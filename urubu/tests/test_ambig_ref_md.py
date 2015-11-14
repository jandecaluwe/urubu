import os
from urubu import UrubuError, project
from urubu.md_extensions import _error

from urubu.tests import cd, raises_kind

def test_ambig_ref_md():
    with cd('ambig_ref_md'):
        with raises_kind(UrubuError, _error.ambig_ref_md):
            project.build()
