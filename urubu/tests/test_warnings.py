import os
import pytest
from urubu import UrubuWarning, _warning, project

from urubu.tests import cd

def test_no_yamlfm():
    with cd('no_yamlfm'):
        with pytest.warns(UrubuWarning) as record:
            project.build()
        assert len(record) == 1
        assert _warning.no_yamlfm in str(record[0].message)

def test_undef_tag_layout():
    with cd('undef_tag_layout'):
        with pytest.warns(UrubuWarning) as record:
            project.build()
        assert len(record) == 1
        assert _warning.undef_tag_layout in str(record[0].message)

