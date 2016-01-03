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

def test_ambig_ref_md():
    with cd('ambig_ref_md'):
        with raises_kind(UrubuError, _error.ambig_ref_md):
            project.build()

def test_ambig_refid():
    with cd('ambig_refid'):
        with raises_kind(UrubuError, _error.ambig_refid):
            project.build()

def test_ambig_ref():
    with cd('ambig_ref'):
        with raises_kind(UrubuError, _error.ambig_ref):
            project.build()

def test_date_format():
    with cd('date_format'):
        with raises_kind(UrubuError, _error.date_format):
            project.build()

def test_undef_reflink_title():
    with cd('undef_reflink_title'):
        with raises_kind(UrubuError, _error.undef_reflink_key):
            project.build()

def test_undef_reflink_url():
    with cd('undef_reflink_url'):
        with raises_kind(UrubuError, _error.undef_reflink_key):
            project.build()

def test_ignore_patterns():
    with cd('ignore_patterns'):
        project.build()
        assert not os.path.exists(os.path.join('_build', 'README.html'))
        assert os.path.exists(os.path.join('_build', 'page.html'))

def test_undef_content():
    with cd('undef_content'):
        with raises_kind(UrubuError, _error.undef_content):
            project.build()

def test_undef_key():
    with cd('undef_key'):
        with raises_kind(UrubuError, _error.undef_key):
            project.build()

def test_undef_layout():
    with cd('undef_layout'):
        with raises_kind(UrubuError, _error.undef_info):
            project.build()

def test_undef_ref():
    with cd('undef_ref'):
        with raises_kind(UrubuError, _error.undef_ref):
            project.build()

def test_no_index():
    with cd('no_index'):
        with raises_kind(UrubuError, _error.no_index):
            project.build()


