import os
import pytest
from urubu import UrubuWarning, project
from urubu.md_extensions import _warning

from urubu.tests import cd, raises_kind

def test_undef_ref_md():
    with cd('undef_ref_md'):
        with pytest.warns(UrubuWarning) as record:
            project.build()
        assert len(record) == 1
        assert _warning.undef_ref_md in str(record[0].message)

